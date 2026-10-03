// Fill out your copyright notice in the Description page of Project Settings.


#include "MateCharacter.h"
#include "AudioMixerBlueprintLibrary.h"
#include "Components/InputComponent.h"
#include "Engine/World.h"
#include "Kismet/GameplayStatics.h"
#include "EnhancedInputComponent.h"
#include "SNegativeActionButton.h"

// Sets default values
AMateCharacter::AMateCharacter()
{
	// Set this character to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;
}

void AMateCharacter::Dash()
{
	UE_LOG(LogTemp, Warning, TEXT("Dash trigger"));
	FVector ForwardDirection = GetActorForwardVector();
	LaunchCharacter(ForwardDirection * DashSpeed, true, true);
	
}

// Called when the game starts or when spawned
void AMateCharacter::BeginPlay()
{
	Super::BeginPlay();

	Leader = UGameplayStatics::GetPlayerCharacter(GetWorld(), 0);
	UE_LOG(LogTemp, Warning, TEXT("%s BeginPlay / Leader : %s"), *GetName(),
	       Leader ? *Leader->GetName() : TEXT("NULL"));
}

// Called every frame
void AMateCharacter::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	FVector location = Leader->GetActorLocation();
	FVector targetPosition = location + LeaderFollowOffset;

	FVector MyPosition = GetActorLocation();
	FVector MoveDirection = targetPosition - MyPosition;
	MoveDirection = MoveDirection.GetSafeNormal();

	UE_LOG(LogTemp, Warning, TEXT("%s"), *GetName());
	SetActorLocation(MyPosition + MoveDirection * FollowSpeed * DeltaTime);
}


// Called to bind functionality to input
void AMateCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	Super::SetupPlayerInputComponent(PlayerInputComponent);

	UEnhancedInputComponent* EnhancedInputComponent = Cast<UEnhancedInputComponent>(PlayerInputComponent);
	if (EnhancedInputComponent)
	{
		EnhancedInputComponent->BindAction(DashAction, ETriggerEvent::Started, this, &AMateCharacter::Dash);
	}
}

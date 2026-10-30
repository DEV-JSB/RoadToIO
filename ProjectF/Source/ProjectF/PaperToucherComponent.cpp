// Fill out your copyright notice in the Description page of Project Settings.


#include "PaperToucherComponent.h"
#include "GameFramework/Character.h"
#include "Components/SkeletalMeshComponent.h"
#include "DrawDebugHelpers.h"

// Sets default values for this component's properties
UPaperToucherComponent::UPaperToucherComponent()
{
	// Set this component to be initialized when the game starts, and to be ticked every frame.  You can turn these features
	// off to improve performance if you don't need them.
	PrimaryComponentTick.bCanEverTick = true;

	// ...
}


// Called when the game starts
void UPaperToucherComponent::BeginPlay()
{
	Super::BeginPlay();

	ACharacter* OwnerCharacter = Cast<ACharacter>(GetOwner());
	
	if (!IsValid(OwnerCharacter))
	{
		UE_LOG(LogTemp, Warning, TEXT("Character is invalid"));
		SetComponentTickEnabled(false);
		return;
	}
	
	OwnerMesh = OwnerCharacter->GetMesh();
	if (!IsValid(OwnerMesh) || !OwnerMesh->DoesSocketExist(BoneName))
	{
		UE_LOG(LogTemp, Warning, TEXT("Mesh doesn't exist"));
		SetComponentTickEnabled(false);
		return;
	}
	
	
	PartPos = OwnerMesh->GetSocketLocation(BoneName);
	PrevPartPos = PartPos;
	
}


// Called every frame
void UPaperToucherComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);
	
	if (DeltaTime <= 0.f)
	{
		return;
	}
	
	
	PartPos = OwnerMesh->GetSocketLocation(BoneName);
	PartVel = (PartPos - PrevPartPos) / DeltaTime;
	PrevPartPos = PartPos;
	
	if (bDrawDebug)
	{
		DrawDebugSphere(GetWorld(),PartPos,TouchRadius,12,FColor::Cyan);
		if (GEngine)
		{
			GEngine->AddOnScreenDebugMessage(static_cast<int32>(GetUniqueID()), 0.f, FColor::Cyan,
			                                 FString::Printf(
				                                 TEXT("%s %s speed = %.0f"), *GetOwner()->GetName(),
				                                 *BoneName.ToString(), PartVel.Size()));
		}
	}
}


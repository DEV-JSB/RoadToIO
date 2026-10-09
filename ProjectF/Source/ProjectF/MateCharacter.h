// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Character.h"
#include "MateCharacter.generated.h"


class UInputAction;
class UAnimMontage;

UCLASS()
class PROJECTF_API AMateCharacter : public ACharacter
{
	GENERATED_BODY()

public:
	// Sets default values for this character's properties
	AMateCharacter();

public:
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly)
	bool bIsDashing;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly)
	bool bIsSprinting;
	
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly)
	UCharacterMovementComponent* MovementComponent;
	
	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	float SprintSpeed;
	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	float WalkSpeed;
	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	bool IsFollowLeader;
	
	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	float FollowSpeed;
	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	float DashSpeed;
	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	float DashDuration;

	UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Input")
	UInputAction* DashAction;
	UPROPERTY(EditAnywhere, BlueprintReadWrite)
	UAnimMontage* DashMontage;

	UPROPERTY(BlueprintReadWrite, EditAnywhere)
	FVector LeaderFollowOffset;
	
	FTimerHandle DashTimerHandle;
	
private:
	ACharacter* Leader;

private:
	void Dash();
	void EndDash();
	void StopSprint();
	void FollowLeader(float DeltaTime);
	void SetMovementMaxWalkSpeed(float MoveSpeed);
protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;

public:	
	// Called every frame
	virtual void Tick(float DeltaTime) override;

	// Called to bind functionality to input
	virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;

};

// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "PaperToucherComponent.generated.h"


class USkeletalMeshComponent;

UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent))
class PROJECTF_API UPaperToucherComponent : public UActorComponent
{
	GENERATED_BODY()

public:	
	// Sets default values for this component's properties
	UPaperToucherComponent();

public:
	UPROPERTY(EditAnywhere,Category="PaperToucher")
	FName BoneName = TEXT("foot_l");
	UPROPERTY(EditAnywhere,Category="PaperToucher")
	float TouchRadius = 15.f;
	UPROPERTY(EditAnywhere,Category="PaperToucher")
	bool bDrawDebug = true;
	
	
	UPROPERTY(VisibleAnywhere,BlueprintReadOnly,Category="PaperToucher")
	FVector PartPos = FVector::ZeroVector;
	UPROPERTY(VisibleAnywhere,BlueprintReadOnly,Category="PaperToucher")
	FVector PartVel = FVector::ZeroVector;

private:
	UPROPERTY()
	TObjectPtr<USkeletalMeshComponent> OwnerMesh;
	
	FVector PrevPartPos = FVector::ZeroVector;
protected:
	// Called when the game starts
	virtual void BeginPlay() override;

public:	
	// Called every frame
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;

		
};

from pydantic import BaseModel
from fastapi import Form

class ArtworkRequest(BaseModel):
    # === Artwork Information ===
    artistLastName: str
    artistFirstName: str
    title: str
    yearCompleted: str
    size: str
    usualType: str
    otherType: str = ""
    usualMedium: str
    otherMedium: str = ""
    usualStyle: str
    otherStyle: str = ""

    # === Owner Information === (all optional)
    ownerSSN: str = ""
    ownerLastName: str = ""
    ownerFirstName: str = ""
    ownerStreet: str = ""
    ownerCity: str = ""
    ownerState: str = ""
    ownerZip: str = ""
    ownerAreaCode: str = ""
    ownerPhoneNumber: str = ""

    # === Gallery Information ===
    dateListed: str
    askingPrice: str
    status: str

    @classmethod
    def as_form(
        cls,
        artistLastName: str = Form(...),
        artistFirstName: str = Form(...),
        title: str = Form(...),
        yearCompleted: str = Form(...),
        size: str = Form(...),
        usualType: str = Form(...),
        otherType: str = Form(""),
        usualMedium: str = Form(...),
        otherMedium: str = Form(""),
        usualStyle: str = Form(...),
        otherStyle: str = Form(""),
        ownerSSN: str = Form(""),
        ownerLastName: str = Form(""),
        ownerFirstName: str = Form(""),
        ownerStreet: str = Form(""),
        ownerCity: str = Form(""),
        ownerState: str = Form(""),
        ownerZip: str = Form(""),
        ownerAreaCode: str = Form(""),
        ownerPhoneNumber: str = Form(""),
        dateListed: str = Form(...),
        askingPrice: str = Form(...),
        status: str = Form(...)
    ):
        return cls(
            artistLastName=artistLastName,
            artistFirstName=artistFirstName,
            title=title,
            yearCompleted=yearCompleted,
            size=size,
            usualType=usualType,
            otherType=otherType,
            usualMedium=usualMedium,
            otherMedium=otherMedium,
            usualStyle=usualStyle,
            otherStyle=otherStyle,
            ownerSSN=ownerSSN,
            ownerLastName=ownerLastName,
            ownerFirstName=ownerFirstName,
            ownerStreet=ownerStreet,
            ownerCity=ownerCity,
            ownerState=ownerState,
            ownerZip=ownerZip,
            ownerAreaCode=ownerAreaCode,
            ownerPhoneNumber=ownerPhoneNumber,
            dateListed=dateListed,
            askingPrice=askingPrice,
            status=status
        )

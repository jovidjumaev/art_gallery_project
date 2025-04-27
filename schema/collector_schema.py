from pydantic import BaseModel
from fastapi import Form

class CollectorRequest(BaseModel):
    # Interview Information
    interviewDate: str
    interviewerName: str

    # Personal Information
    lastName: str
    firstName: str
    street: str
    city: str
    state: str
    zip: str
    areaCode: str
    telephoneNumber: str
    socialSecurityNumber: str

    # Collection Information
    collectionArtistLastName: str = ""
    collectionArtistFirstName: str = ""
    collectionType: str = ""
    otherTypeInput: str = ""
    collectionMedium: str = ""
    otherMediumInput: str = ""
    collectionStyle: str = ""
    otherStyleInput: str = ""

    # 🎯 Sales info (added now)
    salesLastYear: float = 0.0
    salesYearToDate: float = 0.0

    @classmethod
    def as_form(
        cls,
        interviewDate: str = Form(...),
        interviewerName: str = Form(...),
        lastName: str = Form(...),
        firstName: str = Form(...),
        street: str = Form(...),
        city: str = Form(...),
        state: str = Form(...),
        zip: str = Form(...),
        areaCode: str = Form(...),
        telephoneNumber: str = Form(...),
        socialSecurityNumber: str = Form(...),
        collectionArtistLastName: str = Form(""),
        collectionArtistFirstName: str = Form(""),
        collectionType: str = Form(""),
        otherTypeInput: str = Form(""),
        collectionMedium: str = Form(""),
        otherMediumInput: str = Form(""),
        collectionStyle: str = Form(""),
        otherStyleInput: str = Form(""),
        salesLastYear: float = Form(0.0),
        salesYearToDate: float = Form(0.0)
    ):
        return cls(
            interviewDate=interviewDate,
            interviewerName=interviewerName,
            lastName=lastName,
            firstName=firstName,
            street=street,
            city=city,
            state=state,
            zip=zip,
            areaCode=areaCode,
            telephoneNumber=telephoneNumber,
            socialSecurityNumber=socialSecurityNumber,
            collectionArtistLastName=collectionArtistLastName,
            collectionArtistFirstName=collectionArtistFirstName,
            collectionType=collectionType,
            otherTypeInput=otherTypeInput,
            collectionMedium=collectionMedium,
            otherMediumInput=otherMediumInput,
            collectionStyle=collectionStyle,
            otherStyleInput=otherStyleInput,
            salesLastYear=salesLastYear,
            salesYearToDate=salesYearToDate
        )

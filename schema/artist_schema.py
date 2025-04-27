from pydantic import BaseModel
from typing import Optional
from fastapi import Form

class ArtistRequest(BaseModel):
    interviewDate: str
    interviewerName: str
    firstName: str
    lastName: str
    street: str
    zip: str
    areaCode: str
    telephoneNumber: str
    socialSecurityNumber: str
    usualMedium: str
    otherMedium: Optional[str] = None
    usualStyle: str
    otherStyle: Optional[str] = None
    usualType: str
    otherType: Optional[str] = None

    @classmethod
    def as_form(
        cls,
        interviewDate: str = Form(...),
        interviewerName: str = Form(...),
        firstName: str = Form(...),
        lastName: str = Form(...),
        street: str = Form(...),
        zip: str = Form(...),
        areaCode: str = Form(...),
        telephoneNumber: str = Form(...),
        socialSecurityNumber: str = Form(...),
        usualMedium: str = Form(...),
        otherMedium: Optional[str] = Form(None),
        usualStyle: str = Form(...),
        otherStyle: Optional[str] = Form(None),
        usualType: str = Form(...),
        otherType: Optional[str] = Form(None),
    ):
        return cls(
            interviewDate=interviewDate,
            interviewerName=interviewerName,
            firstName=firstName,
            lastName=lastName,
            street=street,
            zip=zip,
            areaCode=areaCode,
            telephoneNumber=telephoneNumber,
            socialSecurityNumber=socialSecurityNumber,
            usualMedium=usualMedium,
            otherMedium=otherMedium,
            usualStyle=usualStyle,
            otherStyle=otherStyle,
            usualType=usualType,
            otherType=otherType
        )

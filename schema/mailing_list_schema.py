from pydantic import BaseModel
from fastapi import Form

class MailingListRequest(BaseModel):
    signupDate: str
    firstName: str
    lastName: str
    areaCode: str
    telephoneNumber: str
    street: str
    zip: str
    preferredArtistFirstName: str = ""
    preferredArtistLastName: str = ""
    preferredMedium: str = ""
    preferredStyle: str = ""
    preferredType: str = ""

    @classmethod
    def as_form(
        cls,
        signupDate: str = Form(...),
        firstName: str = Form(...),
        lastName: str = Form(...),
        areaCode: str = Form(...),
        telephoneNumber: str = Form(...),
        street: str = Form(...),
        zip: str = Form(...),
        preferredArtistFirstName: str = Form(""),
        preferredArtistLastName: str = Form(""),
        preferredMedium: str = Form(""),
        preferredStyle: str = Form(""),
        preferredType: str = Form("")
    ):
        return cls(
            signupDate=signupDate,
            firstName=firstName,
            lastName=lastName,
            areaCode=areaCode,
            telephoneNumber=telephoneNumber,
            street=street,
            zip=zip,
            preferredArtistFirstName=preferredArtistFirstName,
            preferredArtistLastName=preferredArtistLastName,
            preferredMedium=preferredMedium,
            preferredStyle=preferredStyle,
            preferredType=preferredType
        )

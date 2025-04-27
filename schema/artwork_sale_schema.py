from pydantic import BaseModel
from typing import Optional
from fastapi import Form

class ArtworkSaleRequest(BaseModel):
    # Artwork Info
    artworkTitle: str
    artistLastName: str
    artistFirstName: str

    # Owner Info (optional)
    ownerLastName: Optional[str] = None
    ownerFirstName: Optional[str] = None
    ownerStreet: Optional[str] = None
    ownerCity: Optional[str] = None
    ownerState: Optional[str] = None
    ownerZip: Optional[str] = None
    ownerAreaCode: Optional[str] = None
    ownerPhoneNumber: Optional[str] = None

    # Buyer Info
    buyerLastName: str
    buyerFirstName: str
    buyerStreet: str
    buyerCity: str
    buyerState: str
    buyerZip: str
    buyerAreaCode: str
    buyerPhoneNumber: str

    # Payment Info
    salePrice: float
    saleTax: float
    amountRemittedToOwner: float

    # Salesperson Info
    salespersonSSN: str
    saleDate: str

    @classmethod
    def as_form(
        cls,
        artworkTitle: str = Form(...),
        artistLastName: str = Form(...),
        artistFirstName: str = Form(...),
        
        ownerLastName: Optional[str] = Form(None),
        ownerFirstName: Optional[str] = Form(None),
        ownerStreet: Optional[str] = Form(None),
        ownerCity: Optional[str] = Form(None),
        ownerState: Optional[str] = Form(None),
        ownerZip: Optional[str] = Form(None),
        ownerAreaCode: Optional[str] = Form(None),
        ownerPhoneNumber: Optional[str] = Form(None),

        buyerLastName: str = Form(...),
        buyerFirstName: str = Form(...),
        buyerStreet: str = Form(...),
        buyerCity: str = Form(...),
        buyerState: str = Form(...),
        buyerZip: str = Form(...),
        buyerAreaCode: str = Form(...),
        buyerPhoneNumber: str = Form(...),

        salePrice: float = Form(...),
        saleTax: float = Form(...),
        amountRemittedToOwner: float = Form(...),

        salespersonSSN: str = Form(...),
        saleDate: str = Form(...)
    ):
        return cls(
            artworkTitle=artworkTitle,
            artistLastName=artistLastName,
            artistFirstName=artistFirstName,
            ownerLastName=ownerLastName,
            ownerFirstName=ownerFirstName,
            ownerStreet=ownerStreet,
            ownerCity=ownerCity,
            ownerState=ownerState,
            ownerZip=ownerZip,
            ownerAreaCode=ownerAreaCode,
            ownerPhoneNumber=ownerPhoneNumber,
            buyerLastName=buyerLastName,
            buyerFirstName=buyerFirstName,
            buyerStreet=buyerStreet,
            buyerCity=buyerCity,
            buyerState=buyerState,
            buyerZip=buyerZip,
            buyerAreaCode=buyerAreaCode,
            buyerPhoneNumber=buyerPhoneNumber,
            salePrice=salePrice,
            saleTax=saleTax,
            amountRemittedToOwner=amountRemittedToOwner,
            salespersonSSN=salespersonSSN,
            saleDate=saleDate
        )

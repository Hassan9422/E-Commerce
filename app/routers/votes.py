from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import session

from app import schemas, database, OAuth2, models

router = APIRouter(
    prefix="/votes", tags=["Votes"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote_one_product(vote: schemas.Vote, db: session = Depends(database.get_db), current_user: int = Depends(
    OAuth2.verify_and_get_current_user)):
    found_product = db.query(models.Product).filter(models.Product.id == vote.product_id).first()

    if not found_product:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"product with id={vote.product_id} does not exist!")

    found_vote_query = db.query(models.Vote).filter(models.Vote.product_id == vote.product_id)

    if vote.dir == 0:
        if not found_vote_query.first():
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"product with id={vote.product_id} hasn't been liked already!")
        if found_product.product_owner_id == current_user.id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail=" you can't vote on your own product!")
        found_vote_query.delete(synchronize_session=False)
        db.commit()

        return {"detail": "you deleted your vote successfully!"}

    else:
        if found_vote_query.first():
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"product with id={vote.product_id} has been liked already!")

        if found_product.product_owner_id == current_user.id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, detail=" you can't vote on your own product!")

        new_vote = models.Vote(product_id=vote.product_id, user_id=current_user.id)

        db.add(new_vote)
        db.commit()

        return {"detail": "you voted successfully!"}



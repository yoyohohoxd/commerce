# Commerce website for Web50

## Notes

1. A user can close its own listing and therefore be the "winner". This is intended in case the user should want to close the listing

## To-Do List

1. Create error/warning if incorrect data has been input to create_listing page, resulting in no entry to db

2. ~~Save categories in models.py instead of a line in top of views.py. This should also fix category-unusuality in the create_listing function~~

3. Remove quotationmarks from User models referring to listings

4. Make popups on:
    - New listing created
    - Bid succesfully made
    - Bid was unsuccessful due to being too low

5. ~~Fix everything to do with authetication on the listing page~~

6. Redirect instead of response so the user doesn't get stuck in indefinite look
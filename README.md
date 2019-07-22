My Wishlist System
===================
620011825
============


-------------

instructions
-------------
1. install virtualenv and activate environment
2. sudo apt-get install libpq-dev python-dev
3. install requirements.txt
4. create proj3 database and set postgres user password to postgres or configure your own database settings
5. run db migrate -> upgrade
6. register first user and use the system
7. on your user homepage there will be an instructions link, click it for more info on how to use the site. if you see a msg that says resource not available, just try the link again.

Features implemented
--------------------

1. all routes properly named and functioning according to API documentation, I dont return any json data though, just the views
2. Facebook,twitter,email sharing of user's wishlist
3. User cannot add same item/url again
4. most flashed error messages, will present a dismissable flash message
5. all forms have form validation, passwords are hashed
6. user can delete a wish
7. each wish thumbnail is clickable and routes to the original url of the item in the wishlist
8. if user has no wishes a message is displayed and sharing is disabled/hidden. As soon as a wish is added, sharing is enabled
9. Five star rating system implemented. Wishlist is sorted based on rating. Higher rated wishes at top of list
10. wishlist entries are categorized and can be filtered when viewing your wishlist.
11. Logged in user tries to access registration and login routes, they are redirected and a message is displayed. Admin can access registration page. Admin user has email "admin@wishlist.com"
12. Ability to mark items as bought and remove them from main wishlist view. Click on 'view bought items' to load items marked as bought. Click on the link again to load current wishlist
13. Click on user profile image to get a bigger picture, click on your name to return to your personal home screen from anywhere


Confirmed to work on these websites
-----------------------------------
1. Amazon
2. E-Bay
3. Tiger Direct
4. Lenovo
5. Dell
6. Best Buy
7. Newegg
8. times magazine
7. May work on others, not tested. It should work on any site with an image though, even non e-commerce sites


Routes not in API documentation
-------------------------------
1. **"/api/wish/\<id\>/delete" METHOD=GET**  
    Used to delete a wish. Olny input is wish id.I know how this looks but it is secure. Login is required for the route and of the currently 
    logged in user does not match the user who created tthe wish then the user is redirected and a message
    flashed to tell the user not to use the website maliciously. Works great otherwise.
2. **"/api/wish/\<id\>/priority" METHODS=GET,POST**  
    Used to update the rating of a wish. takes wish id and updates record
3. **"/api/wish/\<id\>/bought" METHOD=GET**
    Marks an item as bought. Similar security measure as with the delete route.
4. **"/api/user/update-view" METHOD=POST**
    Filters wishlist view to view only items in the selected category
5. **"/api/user/<id>/wishlist/share" METHOD=POST**
    Emails logged in user's wishlist to email addresses entered by the user.
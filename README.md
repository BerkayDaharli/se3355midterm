Hepsiburada by Berkay

Can be accessed through the following link: https://34.16.238.234:8100 (runs on a very simple GCP Compute Engine, thus loads slow)

**Data Model:**
There are tables for the following: Campaign, Product, Product Color, Image, Category, and City.

Campaign:
- Has title, description, an image file name, a button name, and a link for where to go when the button is pressed.
- The campaigns shown in home page are all constructed using the information above, fetched dynamically from the PostgreSQL database.

Product:
- Has title, description, colors (a one-to-many relationship between ProductColor), category id, and shipped from id.
- All products have at least one color which is the default. If the product has multiple colors, there is no need for the default.
- Shipped from id is used for whether the product is eligible for "Yarın Kapında". The user has to choose a city when browsing the categories or after making a search, and they must enable the "By your doorstep tomorrow" option from the right hand side. Upon doing so, if a product is being shipped from the same city as the what user chose, that (or those) product(s) will be brought to the front, and they will be marked with a green box with the text "By your doorstep tomorrow".

ProductColor:
- Has product id (for linking which product this color is for), the color name, the price, and images (one-to-many relationship between Image)
- Each color can have a different price, and multiple images.

Image:
- Has an image file name, and product color id.

Category:
- Has category name and id

City:
- Has city name and id.

**Assumptions**
- Product descriptions are not changing based on color
- "Yarın Kapında" depends on whether the selected city and where the product is shipped from are the same

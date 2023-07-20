# Playyn - Online Music Store

## Problem statement

Music is an integral part of everyone's lives. We tend to feel many different emotions through music. But nowadays, unless we are suggested songs by some advanced recommendation engine, we tend to miss out on many such tracks, which would potentially be of one's interest. Such interests can be defined by many such criteria, like one prefers instrumentals over vocals, or one can take interest in the **danceability** (having a rhythm and style that people can dance to) of a track. But such information is seldom available publicly. We decide to tackle this problem by showing the users a detailed audio analysis for each track, along with audio features that might take their interest, so that they can decide whether it exactly caters to their interests.

## Description

"Playyn" is an online music store where artists will upload their composed tracks for users all around the world to buy and enjoy. Customers can browse and view advanced analysis of any track, and filter their choice of music before buying. They are also presented with coupon discounts from time to time.

## Account creation

Any artist who wishes to post his or her songs on the website may do so. Individual artists and bands are both permitted to sell music. When making an account, the user is prompted to provide some basic information such as his name, location, email address, and phone number. It also includes an option that indicates if the user is an artist, a band, or just a customer. The user is then prompted to select a username. This username must be unique and meet specific requirements. After selecting a distinct user name, the user is prompted to provide a password that must be at least 8 characters long and should be something difficult to guess. By creating a new row in the database, all of the requested data will be added. The user may now complete their profile by giving information such as their proficiency or band name for the artist, otherwise, a customer may directly proceed to buy tracks.

## Uploading tracks

By meeting some basic conditions, an artist can add a song along with the title of the song, the artist, the genre, whether it is explicit, and the available market. In order to enable the user to be more particular about his criteria, the artist may supply extra information about the music, such as mode, pace, liveness, and speechiness. This allows the customer to better select the song, resulting in a greater predicted sale of the music. These specifics must be obtained from the artist. If the artist is unable to offer this more advanced data, it is collected, if feasible, using Spotify's API, which delivers song specifications based on certain criteria.

## Browsing tracks

With the use of filters, the customer may conveniently navigate through the music library. Based on the filter criteria, the customer can use the filter to display certain titles. The filters will include parameters such as genre, artist, album, duration, and price, among others. When searching, the customer has the option of combining numerous criteria or sorting the presented choice by audio attributes such as duration, tempo, volume, and so on. The user may find exactly the genre of music he wants by using filters and sorting.

## Cart management

The system offers the customer a cart in which to keep the music for which they are ready to pay. This cart is saved in a session and may hold numerous songs, allowing the consumer to buy them all at once. It enables the customer to navigate between websites without changing the cart. The user can then proceed to the checkout page and confirm the payment. This payment can be made through major credit and debit cards. To guarantee consumer rights are protected, card details such as the card Number, expiry date, and CVV are not saved in the database and are just forwarded to the payment provider.

## Objectives

We aspire to accomplish the following:
- Artists should be able to:
	- Create an account by providing some basic information
	- Register as a band or an individual performer
	- Identify themselves as a vocalist and/or an instrumentalist
	- Upload tracks as singles or in an album
	- Retrieve/Edit/Delete any account, track, or album information they have created
- Customers should be able to:
	- Create an account by providing some basic information
	- View a detailed audio analysis for each track
	- Add individual tracks and/or albums to their cart
	- Check out their cart resulting from placing an order
	- Retrieve/Edit/Delete any account or cart information they have created
- Each track should:
	- Belong to one or more genre
	- Be a single or part of an album
	- Store a detailed audio feature analysis
	- Be able to be added to one or more carts/orders
- The platform accounts for browsing capabilities along with managing roles effectively

## Requirements

### Front-end

The graphical user interface of a website, so that users can view and interact with that website. In the client–server model, the client is usually considered the front end.
- **HTML** --- Hypertext Markup Language (HTML) is the standard markup language for creating web pages and web applications. HTML defines the structure and semantics of the web application.
- **CSS** --- Cascading Style Sheets(CSS) is a style-sheet language used to describe the presentation of a document written in HTML. It describes how elements are rendered on screen.
- **JavaScript** --- JavaScript (JS) is a full-fledged dynamic programming language that, when applied to an HTML document, can provide dynamic interactivity on websites. It can be used to control web pages on the client side and even server-side programs.

### Back-end

The data access layer of a piece of the website is ideally done through a framework and database. In the client–server model, the server is usually considered the back end.
- **MySQL** --- MySQL is a  free, open-source relational database management system (RDBMS). 
- **Django** --- Django is a free, open-source, and high-level Python web application framework. It is a collection of python libraries that allow us to quickly and efficiently create web applications and is suitable for both front-end and back-end.

## UML diagram

![UML](/static/img/uml.png?raw=true)

## Activity diagram

### Registering as a new artist

![Artist creation](/static/img/artist-creation.png?raw=true)

### Adding new tracks as an artist

![Adding a track](/static/img/adding-a-track.png?raw=true)

### Purchasing tracks as a user

![Place order](/static/img/place-order.png?raw=true)

## Installation

Please see the following [step-by-step guide](/setup) for seting up a working demo in Windows.

## Additional features

As an extension to this proposal, I also intend to include transactional statistics for both the artist and the customer along with visualizations to better identify the preferences of the user during the filter and sort.

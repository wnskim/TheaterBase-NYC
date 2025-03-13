# William Kim WNK2103
from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from dotenv import load_dotenv

load_dotenv()  # Add this near the top of server.py

app = Flask(__name__)

# Get API key from environment variable
MAPS_KEY = os.environ.get('GOOGLEMAPSKEY')

theaters = {
    "Metrograph": {
        "id": "Metrograph",
        "name": "Metrograph",
        "banner": "https://wnskim.github.io/TheaterBase-NYC/Media/Metrograph/Banner.png",
        "banner_alt": "Banner Image: In the Mood for Love (200)",
        "image": "https://wnskim.github.io/TheaterBase-NYC/Media/Metrograph/Main.png",
        "image_alt": "Interior of Metrograph theater",
        "description": (
            "Metrograph offers a curated selection of art-house and classic films. "
            "It has an old-timey vintage feel that elevates the cinema experience. "
            "The venue also has a bookstore and a stylish cafe. "
            "It's a must-visit for film lovers seeking rare and revival screenings."
        ),
        "address": "7 Ludlow St, New York, NY 10002",
        "ticket price": "$17",
        "student ticket price": "$15",
        "types of movies": ["Art House", "Classic Films", "Foreign", "Repertory", "Food & Drink", "Historic Venue"],
        "nearby theater ids": ["Angelika-Film-Center", "IFC-Center", "Anthology-Film-Archives"],
        "website": "https://metrograph.com/"
    },
    "Film-Forum": {
        "id": "Film-Forum",
        "name": "Film Forum",
        "banner": "https://wnskim.github.io/TheaterBase-NYC/Media/Film-Forum/Banner.png",
        "banner_alt": "Banner Image: Play it as it Lays (1972)",
        "image": "https://wnskim.github.io/TheaterBase-NYC/Media/Film-Forum/Main.png",
        "image_alt": "Exterior of Film Forum at night",
        "description": (
            "Film Forum is known for independent premieres and repertory programs. "
            "It frequently hosts director Q&As and themed film festivals. "
            "Its intimate setting encourages thoughtful discussion among film buffs. "
            "The lineup often includes documentaries, foreign films, and classics."
        ),
        "address": "209 W Houston St, New York, NY 10014",
        "ticket price": "$16",
        "student ticket price": "$10",
        "types of movies": ["Indie", "Foreign", "Classic Films", "Repertory", "Q and A Events", "Festival"],
        "nearby theater ids": ["IFC-Center", "Angelika-Film-Center", "Cinema-Village"],
        "website": "https://filmforum.org/"
    },
    "Angelika-Film-Center": {
        "id": "Angelika-Film-Center",
        "name": "Angelika Film Center",
        "banner": "https://wnskim.github.io/TheaterBase-NYC/Media/Angelika-Film-Center/Banner.png",
        "banner_alt": "Banner Image: Anora (2024)",
        "image": "https://wnskim.github.io/TheaterBase-NYC/Media/Angelika-Film-Center/Main.png",
        "image_alt": "Exterior of Angelika Film Center",
        "description": (
            "Angelika Film Center is a hub for indie flicks and buzzy festival hits. "
            "It has a spacious cafe in the lobby, perfect for casual meetups. "
            "The theater is centrally located, making it popular with students. "
            "Its diverse programming includes documentaries, foreign films, and select blockbusters."
        ),
        "address": "18 W Houston St, New York, NY 10012",
        "ticket price": "$17",
        "student ticket price": "$14",
        "types of movies": ["Indie", "Foreign", "Festival", "New Releases", "Food and Drink", "Student Discounts"],
        "nearby theater ids": ["Film-Forum", "IFC-Center", "Metrograph", "Village-East-by-Angelika"],
        "website": "https://angelikafilmcenter.com/"
    },
    "IFC-Center": {
        "id": "IFC-Center",
        "name": "IFC Center",
        "banner": "https://wnskim.github.io/TheaterBase-NYC/Media/IFC-Center/Banner.png",
        "banner_alt": "Banner Image: Love and Pop (1998)",
        "image": "https://wnskim.github.io/TheaterBase-NYC/Media/IFC-Center/Main.png",
        "image_alt": "Exterior of IFC Center at night",
        "description": (
            "IFC Center is a Greenwich Village staple for cutting-edge cinema. "
            "Its midnight movie series is beloved by cult film aficionados. "
            "They also host engaging post-screening discussions with filmmakers. "
            "Expect everything from indie debuts to Oscar contenders."
        ),
        "address": "323 6th Ave, New York, NY 10014",
        "ticket price": "$16",
        "student ticket price": "$13",
        "types of movies": ["Indie", "Classic Films", "New Releases", "Art House", "Q and A Events", "Special Events"],
        "nearby theater ids": ["Film-Forum", "Cinema-Village", "Angelika-Film-Center"],
        "website": "https://ifccenter.com/"
    },
    "Quad-Cinema": {
        "id": "Quad-Cinema",
        "name": "Quad Cinema",
        "banner": "https://wnskim.github.io/TheaterBase-NYC/Media/Quad-Cinema/Banner.png",
        "banner_alt": "Banner Image: The Lady (2011)",
        "image": "https://wnskim.github.io/TheaterBase-NYC/Media/Quad-Cinema/Main.png",
        "image_alt": "Exterior of QUAD Cinema",
        "description": (
            "Quad Cinema offers a boutique atmosphere with four screens. "
            "Its renovated interior combines classic movie-house charm with modern tech. "
            "Programming ranges from international art films to American indie gems. "
            "Frequent special events include retrospectives and director spotlights."
        ),
        "address": "34 W 13th St, New York, NY 10011",
        "ticket price": "$16",
        "student ticket price": "$13",
        "types of movies": ["Art House", "Indie", "Foreign", "Repertory", "Special Events", "Historic Venue"],
        "nearby theater ids": ["IFC-Center", "Nitehawk-Cinema"],
        "website": "https://quadcinema.com/"
    },
    "Nitehawk-Cinema": {
        "id": "Nitehawk-Cinema",
        "name": "Nitehawk Cinema",
        "banner": "https://wnskim.github.io/TheaterBase-NYC/Media/Nitehawk-Cinema/Banner.png",
        "banner_alt": "Banner Image: Mickey 17 (2025)",
        "image": "https://wnskim.github.io/TheaterBase-NYC/Media/Nitehawk-Cinema/Main.png",
        "image_alt": "Interior of a theater at Nitehawk Cinema",
        "description": (
            "Nitehawk Cinema pioneered the dine-in indie theater model in NYC. "
            "Guests can enjoy a full menu and craft cocktails during screenings. "
            "They showcase new independent releases, cult classics, and special midnight series. "
            "Its Williamsburg location is a favorite for film and food enthusiasts alike."
        ),
        "address": "136 Metropolitan Ave, Brooklyn, NY 11249",
        "ticket price": "$18",
        "student ticket price": "$15",
        "types of movies": ["Indie", "Classic Films", "New Releases", "Food and Drink", "Full Bar", "Special Events"],
        "nearby theater ids": ["Quad-Cinema", "Roxy-Cinema"],
        "website": "https://nitehawkcinema.com/"
    },
    "Roxy-Cinema": {
        "id": "Roxy-Cinema",
        "name": "Roxy Cinema",
        "banner": "https://wnskim.github.io/TheaterBase-NYC/Media/Roxy-Cinema/Banner.png",
        "banner_alt": "Banner Image: Shadows (1958)",
        "image": "https://wnskim.github.io/TheaterBase-NYC/Media/Roxy-Cinema/Main.png",
        "image_alt": "Interior of a theater at Roxy Cinema",
        "description": (
            "Located in the Roxy Hotel, this cinema exudes a luxurious, vintage vibe. "
            "It programs a mix of classic Hollywood, independent films, and themed double features. "
            "The cozy, intimate space is ideal for those seeking a more upscale moviegoing experience. "
            "Their lounge area is perfect for pre- or post-show drinks."
        ),
        "address": "2 6th Ave, New York, NY 10013",
        "ticket price": "$17",
        "student ticket price": "$17",
        "types of movies": ["Classic Films", "Indie", "Repertory", "Luxury Seating", "Full Bar", "Historic Venue"],
        "nearby theater ids": ["Alamo-Drafthouse-Manhattan", "Film-Forum", "IFC-Center"],
        "website": "https://www.roxyhotelnyc.com/roxy-cinema"
    },
    "Alamo-Drafthouse-Brooklyn": {
        "id": "Alamo-Drafthouse-Brooklyn",
        "name": "Alamo Drafthouse Brooklyn",
        "banner": "https://wnskim.github.io/TheaterBase-NYC/Media/Alamo-Drafthouse-Brooklyn/Banner.png",
        "banner_alt": "Banner Image: Marie Antoinete (2006)",
        "image": "https://wnskim.github.io/TheaterBase-NYC/Media/Alamo-Drafthouse-Brooklyn/Main.png",
        "image_alt": "Interior of an Alamo Drafthouse Brooklyn Theater",
        "description": (
            "Alamo Drafthouse is famed for strict no-talking/no-texting policies. "
            "They serve food and drinks right to your seat, with rotating themed menus. "
            "Expect a mix of big-name films, indie surprises, and fun quote-along events. "
            "This Brooklyn location also hosts special screenings with filmmaker Q&As."
        ),
        "address": "445 Albee Square W, Brooklyn, NY 11201",
        "ticket price": "$18",
        "student ticket price": "$15",
        "types of movies": ["New Releases", "Indie", "Special Events", "Food and Drink", "Full Bar", "Reserved Seating"],
        "nearby theater ids": ["Roxy-Cinema", "Nitehawk-Cinema", "Village-East-by-Angelika"],
        "website": "https://drafthouse.com/nyc"
    },
    "Village-East-by-Angelika": {
        "id": "Village-East-by-Angelika",
        "name": "Village East by Angelika",
        "banner": "https://wnskim.github.io/TheaterBase-NYC/Media/Village-East-by-Angelika/Banner.png",
        "banner_alt": "Banner Image: Look Back (2024)",
        "image": "https://wnskim.github.io/TheaterBase-NYC/Media/Village-East-by-Angelika/Main.png",
        "image_alt": "Interior of a theater in Village East by Angelika",
        "description": (
            "Housed in a historic Moorish Revival building, Village East is a landmark. "
            "It showcases blockbuster releases along with smaller indie titles. "
            "The grand architecture adds a unique flair to the movie experience. "
            "They often host film festivals and special early screenings."
        ),
        "address": "181-189 2nd Ave, New York, NY 10003",
        "ticket price": "$17",
        "student ticket price": "$14",
        "types of movies": ["New Releases", "Indie", "Festival", "Historic Venue", "Special Events"],
        "nearby theater ids": ["Angelika-Film-Center", "Anthology-Film-Archives", "Cinema-Village"],
        "website": "https://angelikafilmcenter.com/villageeast/"
    },
    "The-Paris-Theater": {
        "id": "The-Paris-Theater",
        "name": "The Paris Theater",
        "banner": "https://wnskim.github.io/TheaterBase-NYC/Media/The-Paris-Theater/Banner.png",
        "banner_alt": "Banner Image: Ran (1985)",
        "image": "https://wnskim.github.io/TheaterBase-NYC/Media/The-Paris-Theater/Main.png",
        "image_alt": "Exterior of The Paris Theater at night",
        "description": (
            "The Paris Theater is one of the few remaining single-screen theaters in Manhattan. "
            "It offers a carefully curated selection of art films and upscale premieres. "
            "Known for its elegant interior and timeless charm, it has been a cinephile favorite for decades. "
            "Netflix has used this venue for special theatrical runs of prestige titles."
        ),
        "address": "4 W 58th St, New York, NY 10019",
        "ticket price": "$17",
        "student ticket price": "$17",
        "types of movies": ["Art House", "Classic Films", "Foreign", "Historic Venue", "Luxury Seating"],
        "nearby theater ids": ["Museum-of-Modern-Art", "Film-at-Lincoln-Center"],
        "website": "https://www.theparistheaterny.com/"
    },
    "Film-at-Lincoln-Center": {
        "id": "Film-at-Lincoln-Center",
        "name": "Film at Lincoln Center",
        "banner": "https://wnskim.github.io/TheaterBase-NYC/Media/Film-at-Lincoln-Center/Banner.png",
        "banner_alt": "Banner Image: Winter in Sokcho (2024)",
        "image": "https://wnskim.github.io/TheaterBase-NYC/Media/Film-at-Lincoln-Center/Main.png",
        "image_alt": "Film at Lincoln Center Logo",
        "description": (
            "A cultural landmark dedicated to supporting the art and craft of cinema. "
            "Home to the New York Film Festival and year-round programming. "
            "Features new releases, retrospectives, and special events. "
            "Known for its commitment to film education and preservation."
        ),
        "address": "165 W 65th St, New York, NY 10023",
        "ticket price": "$15",
        "student ticket price": "$12",
        "types of movies": ["Art House", "Festival", "Foreign", "Repertory", "Q and A Events", "Special Events"],
        "nearby theater ids": ["The-Paris-Theater", "Museum-of-Modern-Art"],
        "website": "https://www.filmlinc.org/"
    },
    "Museum-of-Modern-Art": {
        "id": "Museum-of-Modern-Art",
        "name": "Museum of Modern Art (MoMA)",
        "banner": "https://wnskim.github.io/TheaterBase-NYC/Media/Museum-of-Modern-Art/Banner.png",
        "banner_alt": "Banner Image: The Falling Sky (2024)",
        "image": "https://wnskim.github.io/TheaterBase-NYC/Media/Museum-of-Modern-Art/Main.png",
        "image_alt": "Interior of a theater at MoMA",
        "description": (
            "World-renowned museum with dedicated film programming. "
            "Features avant-garde and experimental cinema. "
            "Hosts retrospectives and film preservation screenings. "
            "Home to one of the world's largest film archives."
        ),
        "address": "11 W 53rd St, New York, NY 10019",
        "ticket price": "$25",
        "student ticket price": "$14",
        "types of movies": ["Art House", "Classic Films", "Foreign", "Repertory", "Special Events", "35mm"],
        "nearby theater ids": ["Film-at-Lincoln-Center", "The-Paris-Theater"],
        "website": "https://www.moma.org/film"
    },
    "Nitehawk-Prospect-Park": {
        "id": "Nitehawk-Prospect-Park",
        "name": "Nitehawk Cinema - Prospect Park",
        "banner": "https://wnskim.github.io/TheaterBase-NYC/Media/Nitehawk-Prospect-Park/Banner.png",
        "banner_alt": "Banner Image: The Original Kings of Comedy (2000)",
        "image": "https://wnskim.github.io/TheaterBase-NYC/Media/Nitehawk-Prospect-Park/Main.png",
        "image_alt": "Exterior of Nitehawk Cinema Prospect Park at night",
        "description": (
            "Historic theater renovated into a modern dine-in cinema. "
            "Serves craft food and beverages during screenings. "
            "Shows independent films and special series. "
            "Located in the landmark Pavilion Theater building."
        ),
        "address": "188 Prospect Park West, Brooklyn, NY 11215",
        "ticket price": "$18",
        "student ticket price": "$15",
        "types of movies": ["Indie", "Repertory", "New Releases", "Food and Drink", "Full Bar", "Historic Venue"],
        "nearby theater ids": ["BAM-Rose-Cinemas", "Cobble-Hill-Cinema"],
        "website": "https://nitehawkcinema.com/prospectpark"
    },
    "Angelika-Cinema-123": {
        "id": "Angelika-Cinema-123",
        "name": "Angelika - Cinema 123",
        "banner": "https://wnskim.github.io/TheaterBase-NYC/Media/Angelika-Cinema-123/Banner.png",
        "banner_alt": "Banner Image: Winchester '73 (1950)",
        "image": "https://wnskim.github.io/TheaterBase-NYC/Media/Angelika-Cinema-123/Main.png",
        "image_alt": "Exterior of Cinama 123 by Angelika",
        "description": (
            "Luxury cinema on the Upper East Side. "
            "Features plush recliners and state-of-the-art projection. "
            "Shows a mix of independent and mainstream films. "
            "Known for its intimate atmosphere and premium experience."
        ),
        "address": "1001 3rd Ave, New York, NY 10022",
        "ticket price": "$17",
        "student ticket price": "$14",
        "types of movies": ["Indie", "New Releases", "Art House", "Luxury Seating", "Reserved Seating"],
        "nearby theater ids": ["Museum-of-Modern-Art", "The-Paris-Theater"],
        "website": "https://angelikafilmcenter.com/cinema123"
    },
    "Museum-of-the-Moving-Image": {
        "id": "Museum-of-the-Moving-Image",
        "name": "Museum of the Moving Image",
        "banner": "https://wnskim.github.io/TheaterBase-NYC/Media/Museum-of-the-Moving-Image/Banner.png",
        "banner_alt": "Banner Image: Bonjour Tristesse (2024)",
        "image": "https://wnskim.github.io/TheaterBase-NYC/Media/Museum-of-the-Moving-Image/Main.png",
        "image_alt": "Interior of a theater at Museum of the Moving Image",
        "description": (
            "Dedicated to the art, history, and technology of film and media. "
            "Features a state-of-the-art theater for screenings. "
            "Hosts special exhibitions and film series. "
            "Offers educational programs and workshops."
        ),
        "address": "36-01 35th Ave, Astoria, NY 11106",
        "ticket price": "$15",
        "student ticket price": "$11",
        "types of movies": ["Repertory", "Classic Films", "Foreign", "Special Events", "35mm", "70mm"],
        "nearby theater ids": ["Syndicated", "Anthology-Film-Archives"],
        "website": "https://movingimage.us/"
    },
    "Syndicated": {
        "id": "Syndicated",
        "name": "Syndicated",
        "banner": "https://wnskim.github.io/TheaterBase-NYC/Media/Syndicated/Banner.png",
        "banner_alt": "Banner Image: The Room Next Door (2024)",
        "image": "https://wnskim.github.io/TheaterBase-NYC/Media/Syndicated/Main.png",
        "image_alt": "Interior of Syndicated Theater",
        "description": (
            "Unique combination of cinema, bar, and restaurant. "
            "Shows classic films and cult favorites. "
            "Offers full food and drink service during screenings. "
            "Popular spot for themed movie nights and events."
        ),
        "address": "40 Bogart St, Brooklyn, NY 11206",
        "ticket price": "$11",
        "student ticket price": "$11",
        "types of movies": ["Classic Films", "Indie", "Repertory", "Food and Drink", "Full Bar"],
        "nearby theater ids": ["Museum-of-the-Moving-Image", "BAM-Rose-Cinemas"],
        "website": "https://syndicatedbk.com/"
    },
    "BAM-Rose-Cinemas": {
        "id": "BAM-Rose-Cinemas",
        "name": "BAM Rose Cinemas",
        "banner": "https://wnskim.github.io/TheaterBase-NYC/Media/BAM-Rose-Cinemas/Banner.png",
        "banner_alt": "Banner Image: Us and the Night (2024)",
        "image": "https://wnskim.github.io/TheaterBase-NYC/Media/BAM-Rose-Cinemas/Main.png",
        "image_alt": "Interior showing theater seating",
        "description": (
            "Part of the Brooklyn Academy of Music's cultural complex. "
            "Four screens showing independent and repertory films. "
            "Known for innovative programming and film festivals. "
            "Historic venue with modern amenities."
        ),
        "address": "30 Lafayette Ave, Brooklyn, NY 11217",
        "ticket price": "$17",
        "student ticket price": "$12",
        "types of movies": ["Indie", "Repertory", "Festival", "Foreign", "Historic Venue", "Special Events"],
        "nearby theater ids": ["Cobble-Hill-Cinema", "Nitehawk-Prospect-Park", "Alamo-Drafthouse-Brooklyn"],
        "website": "https://www.bam.org/film"
    },
    "Cinema-Village": {
        "id": "Cinema-Village",
        "name": "Cinema Village",
        "banner": "https://wnskim.github.io/TheaterBase-NYC/Media/Cinema-Village/Banner.png",
        "banner_alt": "Banner Image: Flow (2024)",
        "image": "https://wnskim.github.io/TheaterBase-NYC/Media/Cinema-Village/Main.png",
        "image_alt": "Exterior of Cinema Village",
        "description": (
            "One of New York's oldest continuously operating art houses. "
            "Three screens featuring independent and foreign films. "
            "Historic Greenwich Village location since 1963. "
            "Known for showing unique and overlooked films."
        ),
        "address": "22 E 12th St, New York, NY 10003",
        "ticket price": "$13",
        "student ticket price": "$8",
        "types of movies": ["Indie", "Foreign", "Art House", "Historic Venue", "Student Discounts"],
        "nearby theater ids": ["IFC-Center", "Village-East-by-Angelika", "Angelika-Film-Center"],
        "website": "https://www.cinemavillage.com/"
    },
    "Alamo-Drafthouse-Manhattan": {
        "id": "Alamo-Drafthouse-Manhattan",
        "name": "Alamo Drafthouse - Lower Manhattan",
        "banner": "https://wnskim.github.io/TheaterBase-NYC/Media/Alamo-Drafthouse-Manhattan/Banner.png",
        "banner_alt": "Banner Image: Wild at Heart (1990)",
        "image": "https://wnskim.github.io/TheaterBase-NYC/Media/Alamo-Drafthouse-Manhattan/Main.png",
        "image_alt": "Interior of an Alamo Drafthouse Manhattan Theater",
        "description": (
            "Latest addition to the Alamo Drafthouse family in NYC. "
            "Features dine-in service with craft food and beverages. "
            "State-of-the-art projection and sound systems. "
            "Known for special events and themed screenings."
        ),
        "address": "28 Liberty St, New York, NY 10005",
        "ticket price": "$18",
        "student ticket price": "$15",
        "types of movies": ["New Releases", "Indie", "Repertory", "Food and Drink", "Full Bar", "Reserved Seating"],
        "nearby theater ids": ["Metrograph", "Roxy-Cinema"],
        "website": "https://drafthouse.com/nyc/theater/lower-manhattan"
    },
    "Anthology-Film-Archives": {
        "id": "Anthology-Film-Archives",
        "name": "Anthology Film Archives",
        "banner": "https://wnskim.github.io/TheaterBase-NYC/Media/Anthology-Film-Archives/Banner.png",
        "banner_alt": "Banner Image: Nightshift (1981)",
        "image": "https://wnskim.github.io/TheaterBase-NYC/Media/Anthology-Film-Archives/Main.png",
        "image_alt": "Historic Photo of Interior Seating",
        "description": (
            "Center for preservation and exhibition of independent film. "
            "Focuses on avant-garde, experimental, and classic cinema. "
            "Houses extensive film and paper archives. "
            "Offers regular screenings of essential cinema."
        ),
        "address": "32 2nd Ave, New York, NY 10003",
        "ticket price": "$13",
        "student ticket price": "$9",
        "types of movies": ["Classic Films", "Art House", "Foreign", "16mm", "35mm", "Historic Venue"],
        "nearby theater ids": ["Metrograph", "Village-East-by-Angelika"],
        "website": "http://anthologyfilmarchives.org/"
    },
    "Stuart-Cinema": {
        "id": "Stuart-Cinema",
        "name": "Stuart Cafe & Cinema",
        "banner": "https://wnskim.github.io/TheaterBase-NYC/Media/Stuart-Cinema/Banner.png",
        "banner_alt": "Banner Image: Snow White (2025)",
        "image": "https://wnskim.github.io/TheaterBase-NYC/Media/Stuart-Cinema/Main.png",
        "image_alt": "Exterior of Stuart Cinema at night",
        "description": (
            "Community-focused independent cinema and cafe. "
            "Screens a mix of indie films and local productions. "
            "Offers affordable tickets and concessions. "
            "Hosts special events and filmmaker showcases."
        ),
        "address": "79 West St, Brooklyn, NY 11222",
        "ticket price": "$12",
        "student ticket price": "$10",
        "types of movies": ["Indie", "New Releases", "Festival", "Food and Drink", "Student Discounts"],
        "nearby theater ids": ["Syndicated", "BAM-Rose-Cinemas"],
        "website": "https://stuartcinema.com/"
    },
    "Cobble-Hill-Cinema": {
        "id": "Cobble-Hill-Cinema",
        "name": "Cobble Hill Cinema",
        "banner": "https://wnskim.github.io/TheaterBase-NYC/Media/Cobble-Hill-Cinema/Banner.png",
        "banner_alt": "Banner Image: The Lodger: A story of the London Fog (1927)",
        "image": "https://wnskim.github.io/TheaterBase-NYC/Media/Cobble-Hill-Cinema/Main.png",
        "image_alt": "Exterior of Cobble Hill Cinemas",
        "description": (
            "Neighborhood movie theater serving Cobble Hill since 1963. "
            "Shows a mix of mainstream and independent films. "
            "Known for affordable prices and family-friendly atmosphere. "
            "Recently renovated with modern amenities."
        ),
        "address": "265 Court St, Brooklyn, NY 11231",
        "ticket price": "$13",
        "student ticket price": "$10",
        "types of movies": ["New Releases", "Indie", "Student Discounts", "Historic Venue"],
        "nearby theater ids": ["BAM-Rose-Cinemas", "Nitehawk-Prospect-Park"],
        "website": "https://cobblehillcinemas.com/"
    }
}

@app.route('/')
def home():
    """
    Home route that displays 3 'featured' or 'popular' theaters.
    The assignment wants these to be dynamically generated in JS,
    but we'll send them from Python to Jinja as well.
    """
    # Select specific theaters for the featured section
    featured_ids = ["Metrograph", "Film-Forum", "IFC-Center"]
    popular_theaters = [theaters[t_id] for t_id in featured_ids]

    return render_template('home.html', popular_theaters=popular_theaters)

@app.route('/search')
def search():
    query = request.args.get("q", "")
    query = query.strip()
    
    # Normalize the query by replacing 'and' with '&' and converting to lowercase
    query_lower = query.lower()
    query_normalized = query_lower.replace(" and ", " & ")
    
    matching = []
    for t_id, theater_data in theaters.items():
        # Check if query matches theater name
        if query_lower in theater_data["name"].lower():
            matching.append(theater_data)
            continue
            
        # Check if query matches any of the theater's tags
        for tag in theater_data["types of movies"]:
            tag_lower = tag.lower()
            # Normalize the tag for comparison
            tag_normalized = tag_lower.replace(" & ", " and ")
            
            if query_normalized in tag_lower or query_lower in tag_normalized:
                matching.append(theater_data)
                break
    
    return render_template('search.html', query=query, results=matching)


@app.route('/view/<theater_id>')
def view_theater(theater_id):
    if theater_id not in theaters:
        return "Theater not found", 404

    theater_data = theaters[theater_id]
    
    # Get nearby theaters' full data
    nearby_theaters = []
    for nearby_id in theater_data["nearby theater ids"]:
        if nearby_id in theaters:
            nearby_theaters.append(theaters[nearby_id])
    
    return render_template('view.html',
                         theater=theater_data,
                         nearby_theaters=nearby_theaters,
                         maps_key=MAPS_KEY)

@app.route('/add', methods=['GET', 'POST'])
def add_theater():
    if request.method == 'POST':
        # Handle AJAX submission
        data = request.get_json()
        
        # Validate required fields
        errors = {}
        if not data.get('name', '').strip():
            errors['name'] = 'Name is required'
        if not data.get('address', '').strip():
            errors['address'] = 'Address is required'
        if not data.get('description', '').strip():
            errors['description'] = 'Description is required'
            
        if errors:
            return jsonify({'success': False, 'errors': errors}), 400
            
        # Generate new ID from name
        new_id = data['name'].replace(' ', '-')
        if new_id in theaters:
            return jsonify({'success': False, 'errors': {'name': 'A theater with this name already exists'}}), 400
            
        theaters[new_id] = {
            'id': new_id,
            'name': data['name'],
            'address': data['address'],
            'description': data['description'],
            'image': data.get('image', ''),
            'ticket price': data.get('ticket_price', ''),
            'student ticket price': data.get('student_price', ''),
            'types of movies': data.get('movie_types', '').split(','),
            'nearby theater ids': data.get('nearby_ids', '').split(','),
            'website': data.get('website', '')
        }
        
        return jsonify({
            'success': True,
            'id': new_id,
            'message': 'Theater added successfully'
        })
        
    return render_template('add.html')

@app.route('/edit/<theater_id>', methods=['GET', 'POST'])
def edit_theater(theater_id):
    if theater_id not in theaters:
        return "Theater not found", 404
        
    if request.method == 'POST':
        data = request.get_json()
        
        # Similar validation as add route
        errors = {}
        if not data.get('name', '').strip():
            errors['name'] = 'Name is required'
        if errors:
            return jsonify({'success': False, 'errors': errors}), 400
            
        # Update theater data
        theaters[theater_id].update({
            'name': data['name'],
            'address': data['address'],
            'description': data['description'],
            'image': data.get('image', theaters[theater_id]['image']),
            'ticket price': data.get('ticket_price', theaters[theater_id]['ticket price']),
            'student ticket price': data.get('student_price', theaters[theater_id]['student ticket price']),
            'types of movies': data.get('movie_types', '').split(','),
            'nearby theater ids': data.get('nearby_ids', '').split(','),
            'website': data.get('website', theaters[theater_id]['website'])
        })
        
        return jsonify({'success': True, 'message': 'Theater updated successfully'})
        
    return render_template('edit.html', theater=theaters[theater_id])

if __name__ == "__main__":
    app.run(debug=True, port=5001)

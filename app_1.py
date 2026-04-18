from flask import Flask, render_template, redirect, url_for, flash, request
from flask_mail import Mail, Message
from flask_wtf.csrf import CSRFProtect
from config import Config
from forms import ContactForm

app = Flask(__name__)
app.config.from_object(Config)

mail = Mail(app)
csrf = CSRFProtect(app)

PRODUCTS = [
    {
        "id": 1,
        "name": '"Puppy Doll" მაისური — კრემისფერი',
        "description": "კრემისფერი მაისური Puppy Doll პრინტით. ხელმისაწვდომია L ზომაში.",
        "price": "18 ₾ (L)",
        "badge": None,
        "image": "/static/images/01_puppy_doll_cream.jpg",
        "category": "მაისური",
    },
    {
        "id": 2,
        "name": '"Puppy Doll" მაისური — წითელი',
        "description": "წითელი მაისური Puppy Doll პრინტით. ხელმისაწვდომია L ზომაში.",
        "price": "18 ₾ (L)",
        "badge": None,
        "image": "/static/images/02_puppy_doll_red.jpg",
        "category": "მაისური",
    },
    {
        "id": 3,
        "name": "წითელი მაისური",
        "description": "სუფთა წითელი მაისური — კომფორტული და სტილური. L ზომა.",
        "price": "18 ₾ (L)",
        "badge": None,
        "image": "/static/images/03_red_plain.jpg",
        "category": "მაისური",
    },
    {
        "id": 4,
        "name": "საწვიმარი — ყვითელი",
        "description": "ყვითელი წყალგაუმტარი საწვიმარი ზოლიანი შიგნით. S და M ზომები ხელმისაწვდომია.",
        "price": "34 ₾ (S) / 38 ₾ (M)",
        "badge": "ახალი",
        "image": "/static/images/04_raincoat_yellow.jpg",
        "category": "საწვიმარი",
    },
    {
        "id": 5,
        "name": "თბილი მოსაცმელი — ლურჯი (დათვით)",
        "description": "ლამაზი ლურჯი თბილი მოსაცმელი Bear patch-ით. L ზომა.",
        "price": "21 ₾ (L)",
        "badge": None,
        "image": "/static/images/05_warm_blue_bear.jpg",
        "category": "თბილი მოსაცმელი",
    },
    {
        "id": 6,
        "name": "თბილი მოსაცმელი — წითელი (დათვით)",
        "description": "წითელი თბილი მოსაცმელი Bear patch-ით. L ზომა.",
        "price": "21 ₾ (L)",
        "badge": None,
        "image": "/static/images/06_warm_red_bear.jpg",
        "category": "თბილი მოსაცმელი",
    },
    {
        "id": 7,
        "name": "ზოლიანი კაბა — ნარინჯისფერი",
        "description": "ნარინჯისფერი ზოლიანი კაბა შავი ბანტებით. S და M ზომები.",
        "price": "16 ₾ (S) / 18 ₾ (M)",
        "badge": None,
        "image": "/static/images/07_striped_dress_orange.jpg",
        "category": "კაბა",
    },
    {
        "id": 8,
        "name": "გულებიანი კაბა — თეთრი",
        "description": "თეთრი კაბა წითელი გულებით და ლამაზი ბანტით. XXL ზომა.",
        "price": "15 ₾ (XXL)",
        "badge": None,
        "image": "/static/images/08_heart_dress_white.jpg",
        "category": "კაბა",
    },
    {
        "id": 9,
        "name": "გულებიანი ორეული — წითელი",
        "description": "წითელი გულებიანი მაისური + წითელი ქვედა ბოლო. მაისური: S-13₾, M-14₾ | ქვედა ბოლო (S/M/L/XL): 9₾ | ორივე ერთად: S-22₾, M-23₾.",
        "price": "ორივე: 22 ₾ (S) / 23 ₾ (M)",
        "badge": "ბესტსელერი",
        "image": "/static/images/09_heart_set_red.jpg",
        "category": "ორეული",
    },
    {
        "id": 10,
        "name": "ვარდისფერი საყელო ყვავილით",
        "description": "ლამაზი ვარდისფერი საყელო ყვავილის დეკორით. პატარა ძაღლებისთვის.",
        "price": "7 ₾",
        "badge": None,
        "image": "/static/images/10_pink_collar_flower.jpg",
        "category": "საყელო",
    },
    {
        "id": 11,
        "name": "ფერადი ზოლიანი სვიტრი",
        "description": "მრავალფერიანი ზოლიანი სვიტრი — წითელი საყელო, მწვანე ზოლები, ლურჯი და ყვითელი დეტალები. S და M ზომები.",
        "price": "24 ₾ (S) / 27 ₾ (M)",
        "badge": None,
        "image": "/static/images/11_colorful_striped_sweater.jpg",
        "category": "სვიტრი",
    },
    {
        "id": 12,
        "name": "საზაფხულო ჟაკეტი — ლურჯი",
        "description": "ლურჯ-თეთრი ზოლიანი საზაფხულო ჟაკეტი საზღვაო სტილში. L ზომა.",
        "price": "23 ₾ (L)",
        "badge": None,
        "image": "/static/images/12_summer_jacket_blue.jpg",
        "category": "ჟაკეტი",
    },
    {
        "id": 13,
        "name": "საზაფხულო ჟაკეტი — წითელი",
        "description": "წითელ-თეთრი ზოლიანი საზაფხულო ჟაკეტი საზღვაო სტილში. L ზომა.",
        "price": "23 ₾ (L)",
        "badge": None,
        "image": "/static/images/13_summer_jacket_red.jpg",
        "category": "ჟაკეტი",
    },
    {
        "id": 14,
        "name": "საყელო გრძელი ბაფთით",
        "description": "ლურჯი საყელო წითელ-თეთრი კვადრატული ბაფთით. Cotton Soft, ხელნაკეთი. M და L ზომები.",
        "price": "9 ₾ (M) / 12 ₾ (L)",
        "badge": "ახალი",
        "image": "/static/images/14_collar_bow.jpg",
        "category": "საყელო",
    },
]

CATEGORIES = ["ყველა"] + sorted(set(p["category"] for p in PRODUCTS))


@app.route("/")
def index():
    featured = [p for p in PRODUCTS if p["badge"]][:3]
    return render_template("index.html", featured=featured)


@app.route("/shop")
def shop():
    cat = request.args.get("cat", "ყველა")
    if cat == "ყველა":
        products = PRODUCTS
    else:
        products = [p for p in PRODUCTS if p["category"] == cat]
    return render_template("shop.html", products=products, categories=CATEGORIES, active_cat=cat)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            msg = Message(
                subject=f"[PAWLY] {form.subject.data} — {form.name.data}",
                sender=app.config["MAIL_USERNAME"],
                recipients=[app.config["MAIL_RECEIVER"]],
                body=(
                    f"სახელი: {form.name.data}\n"
                    f"ელ-ფოსტა: {form.email.data}\n"
                    f"ტელეფონი: {form.phone.data or '—'}\n"
                    f"თემა: {form.subject.data}\n\n"
                    f"{form.message.data}"
                ),
            )
            mail.send(msg)
            flash("შეტყობინება წარმატებით გაიგზავნა! მალე დაგიკავშირდებით. 🐾", "success")
        except Exception as e:
            app.logger.error(f"Mail error: {e}")
            flash("შეცდომა. გთხოვთ სცადოთ მოგვიანებით ან დაგვიკავშირდეთ პირდაპირ.", "danger")
        return redirect(url_for("contact"))
    return render_template("contact.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)

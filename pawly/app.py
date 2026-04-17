from flask import Flask, render_template, redirect, url_for, flash, request
from flask_mail import Mail, Message
from flask_wtf.csrf import CSRFProtect
from config import Config
from forms import ContactForm

app = Flask(__name__)
app.config.from_object(Config)

mail = Mail(app)
csrf = CSRFProtect(app)

# ---- Product catalogue (add photos later) ----
PRODUCTS = [
    {
        "id": 1,
        "name": "საზღვაო ჟაკეტი",
        "description": "ბიჭური საზღვაო სტილის ჟაკეტი თქვენი ძაღლისთვის. ხელმისაწვდომია XS-XXL ზომებში.",
        "price": "45 ₾",
        "badge": "ახალი",
        "image": "https://placehold.co/400x400/1a3a5c/white?text=🐾",
        "category": "ჟაკეტი",
    },
    {
        "id": 2,
        "name": "ჰუდი ლაბა",
        "description": "რბილი ბამბის ჰუდი, სრულყოფილი გრილ დღეებისთვის. ძალიან კომფორტული.",
        "price": "38 ₾",
        "badge": None,
        "image": "https://placehold.co/400x400/2d6a4f/white?text=🐾",
        "category": "ჰუდი",
    },
    {
        "id": 3,
        "name": "გოგოს კაბა — წითელი",
        "description": "მოხდენილი კაბა ლამაზი ბანტით. იდეალური გასეირნებისა და ფოტოსესიისთვის.",
        "price": "42 ₾",
        "badge": "ბესტსელერი",
        "image": "https://placehold.co/400x400/c1121f/white?text=🐾",
        "category": "კაბა",
    },
    {
        "id": 4,
        "name": "წვიმის ქურთუკი — ყვითელი",
        "description": "წყალგაუმტარი ქურთუკი, რომელიც გაახარებს თქვენს ძაღლს წვიმიანი დღეებიც კი.",
        "price": "55 ₾",
        "badge": None,
        "image": "https://placehold.co/400x400/f4a261/white?text=🐾",
        "category": "ქურთუკი",
    },
    {
        "id": 5,
        "name": "სტრიპ სვიტერი",
        "description": "მულტი-ფერიანი ზოლიანი სვიტერი. სტილური და თბილი ზამთრის სეზონზე.",
        "price": "36 ₾",
        "badge": None,
        "image": "https://placehold.co/400x400/457b9d/white?text=🐾",
        "category": "სვიტერი",
    },
    {
        "id": 6,
        "name": "სპორტული ჟილეტი",
        "description": "მსუბუქი ჟილეტი აქტიური ძაღლებისთვის. ორ ფერში ხელმისაწვდომი.",
        "price": "32 ₾",
        "badge": "ფასდაკლება",
        "image": "https://placehold.co/400x400/6d6875/white?text=🐾",
        "category": "ჟილეტი",
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

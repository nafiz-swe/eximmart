
def get_user_profile(user_id):
    # সাধারণত ডাটাবেজ থেকে ইউজার প্রোফাইল নেয়া হয়
    # ডেমো হিসেবে ফিক্সড ডাটা রিটার্ন করছি
    return {
        "user_id": user_id,
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "017XXXXXXXX"
    }

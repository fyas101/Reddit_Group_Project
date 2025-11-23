"""
Utility Functions and Sample Data Generators for Reddit Analysis

This module contains constants, validation functions, and sample data generators
for testing the Reddit analysis function library.

Author: Reddit Analysis Team - INST326
"""

import re
from datetime import datetime, timedelta
from typing import Dict, List, Any
from collections import Counter
import random

# =============================================================================
# Constants and Configuration
# =============================================================================

# Category keywords for post classification
CATEGORY_KEYWORDS = {
    "humor": ["lol", "lmao", "haha", "joke", "funny"],
    "random": ["idk", "random", "whatever"],
    "news": ["alert", "news", "update", "announcement", "diamondback", "report"],
    "academics": ["class", "classes", "exam", "professor", "grade", "gpa", 
                  "study", "midterm", "final", "project", "homework"],
    "advice": ["recommend", "tips", "help", "should i", "question", "advice"],
    "social": ["party", "hangout", "movie", "homecoming", "game", "event"]
}

# Misinformation detection keywords
MISINFORMATION_KEYWORDS = [
    "rumor", "unconfirmed", "heard", "confirmed??", "sources say",
    "reportedly", "breaking", "shocking", "can't believe",
    "conspiracy", "fake news", "scam", "hoax", "allegedly"
]

# Tone detection cues
TONE_CUES = {
    "anger": ['!', 'angry', 'hate', 'worst', 'terrible'],
    "sarcasm": ['yeah right', 'sure', 'totally'],
    "humor": ['lol', 'funny', 'haha'],
    "uncertainty": ['maybe', 'not sure', 'idk', 'perhaps']
}

# Common UMD subreddit topics
UMD_TOPICS = [
    "dining hall", "testudo", "mckeldin", "stamp", "parking",
    "dorm", "schedule", "registration", "tuition", "football",
    "basketball", "housing", "library", "gym", "campus"
]

# Sample usernames
SAMPLE_USERNAMES = [
    "terp_student", "umd_alum", "testudo_fan", "study_buddy",
    "campus_explorer", "dining_critic", "game_watcher", "library_regular",
    "class_helper", "advice_seeker", "news_poster", "event_organizer"
]

# =============================================================================
# Validation Helper Functions
# =============================================================================

def validate_positive_number(value: float, name: str) -> float:
    """Validate that a number is positive."""
    try:
        num_value = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be a number")
    
    if num_value < 0:
        raise ValueError(f"{name} must be non-negative, got {num_value}")
    
    return num_value


def validate_date_string(date_string: str) -> bool:
    """Validate date string format (YYYY-MM-DD or ISO format)."""
    try:
        datetime.fromisoformat(date_string)
        return True
    except ValueError:
        return False


def normalize_word(word: str) -> str:
    """Normalize word by lowercasing and stripping whitespace."""
    return word.strip().lower()


# =============================================================================
# Sample Data Generators
# =============================================================================

def create_sample_post(
    title: str = None,
    text: str = None,
    username: str = None,
    upvotes: int = None,
    comments: int = None,
    category: str = "random",
    tone: str = "neutral",
    is_disinformation: bool = False,
    created_date: datetime = None
) -> Dict[str, Any]:
    """Create a sample Reddit post for testing.
    
    Args:
        title: Post title (auto-generated if None)
        text: Post text content (auto-generated if None)
        username: Post author (random if None)
        upvotes: Number of upvotes (random 0-100 if None)
        comments: Number of comments (random 0-50 if None)
        category: Post category
        tone: Post tone
        is_disinformation: Whether post contains misinformation
        created_date: Post creation date (now if None)
    
    Returns:
        Dict: Sample post data
    
    Examples:
        >>> post = create_sample_post(title="Finals Week Tips")
        >>> print(post['category'])
        'academics'
    """
    if created_date is None:
        created_date = datetime.utcnow()
    
    if username is None:
        username = random.choice(SAMPLE_USERNAMES)
    
    if title is None:
        title = f"Sample post about {random.choice(UMD_TOPICS)}"
    
    if text is None:
        text = f"This is a sample post discussing {random.choice(UMD_TOPICS)}. What do you all think?"
    
    if upvotes is None:
        upvotes = random.randint(0, 100)
    
    if comments is None:
        comments = random.randint(0, 50)
    
    return {
        "title": title,
        "text": text,
        "selftext": text,
        "username": username,
        "upvotes": upvotes,
        "comments": comments,
        "views": upvotes + comments + random.randint(50, 200),
        "category": category,
        "tone": tone,
        "is_disinformation": is_disinformation,
        "created_utc": created_date.isoformat(),
        "timestamp": created_date.isoformat(),
        "url": f"https://reddit.com/r/UMD/post_{random.randint(1000, 9999)}",
        "post_hint": "text"
    }


def create_sample_posts(count: int = 10) -> List[Dict[str, Any]]:
    """Generate multiple sample posts.
    
    Args:
        count: Number of posts to generate
    
    Returns:
        List[Dict]: List of sample posts
    
    Examples:
        >>> posts = create_sample_posts(5)
        >>> len(posts)
        5
    """
    posts = []
    base_date = datetime.utcnow() - timedelta(days=30)
    
    for i in range(count):
        # Vary the date
        post_date = base_date + timedelta(days=random.randint(0, 30))
        
        # Vary categories
        category = random.choice(list(CATEGORY_KEYWORDS.keys()))
        
        # Create post with category-specific content
        keywords = CATEGORY_KEYWORDS[category]
        text = f"Post about {random.choice(keywords)} and {random.choice(UMD_TOPICS)}"
        
        post = create_sample_post(
            text=text,
            category=category,
            created_date=post_date
        )
        posts.append(post)
    
    return posts


def create_academic_post() -> Dict[str, Any]:
    """Create a sample academic-themed post."""
    titles = [
        "CMSC351 exam tips?",
        "Best study spot on campus?",
        "Professor recommendations for INST326?",
        "Finals week schedule help"
    ]
    texts = [
        "Anyone have advice for the upcoming midterm?",
        "Looking for a quiet place to study this week",
        "Which professor would you recommend?",
        "How are you all managing your finals schedule?"
    ]
    
    return create_sample_post(
        title=random.choice(titles),
        text=random.choice(texts),
        category="academics",
        tone="neutral"
    )


def create_humor_post() -> Dict[str, Any]:
    """Create a sample humorous post."""
    titles = [
        "Dining hall food hits different at 2am lol",
        "When you see Testudo on the way to your exam haha",
        "Me trying to find parking be like...",
        "POV: You forgot about your project due at midnight"
    ]
    
    return create_sample_post(
        title=random.choice(titles),
        text="lol this is so funny",
        category="humor",
        tone="humorous"
    )


def create_misinformation_post() -> Dict[str, Any]:
    """Create a sample post with misinformation markers."""
    titles = [
        "BREAKING: Unconfirmed reports about campus",
        "Rumor: Huge announcement coming soon",
        "I heard from sources that...",
        "Allegedly something shocking happened"
    ]
    
    misinfo_text = f"{random.choice(MISINFORMATION_KEYWORDS)} about campus news"
    
    return create_sample_post(
        title=random.choice(titles),
        text=misinfo_text,
        is_disinformation=True,
        tone="uncertain"
    )


def create_sample_user_data(username: str, num_posts: int = 5) -> List[Dict[str, Any]]:
    """Generate sample posts for a specific user.
    
    Args:
        username: Username to generate posts for
        num_posts: Number of posts to create
    
    Returns:
        List[Dict]: List of posts by this user
    """
    posts = []
    for _ in range(num_posts):
        post = create_sample_post(username=username)
        posts.append(post)
    return posts


def create_weekly_sample_data() -> List[Dict[str, Any]]:
    """Generate sample data spanning a week.
    
    Returns:
        List[Dict]: Posts from the past 7 days
    """
    posts = []
    today = datetime.utcnow()
    
    for day in range(7):
        post_date = today - timedelta(days=day)
        num_posts = random.randint(2, 5)
        
        for _ in range(num_posts):
            post = create_sample_post(created_date=post_date)
            posts.append(post)
    
    return posts


def create_semester_sample_data() -> List[Dict[str, Any]]:
    """Generate sample data spanning a semester (15 weeks).
    
    Returns:
        List[Dict]: Posts from across a semester
    """
    posts = []
    start_date = datetime.utcnow() - timedelta(weeks=15)
    
    for week in range(15):
        week_date = start_date + timedelta(weeks=week)
        num_posts = random.randint(10, 30)
        
        for _ in range(num_posts):
            day_offset = random.randint(0, 6)
            post_date = week_date + timedelta(days=day_offset)
            post = create_sample_post(created_date=post_date)
            posts.append(post)
    
    return posts


# =============================================================================
# Formatting Helper Functions
# =============================================================================

def format_engagement_display(upvotes: int, comments: int) -> str:
    """Format engagement metrics for display.
    
    Args:
        upvotes: Number of upvotes
        comments: Number of comments
    
    Returns:
        str: Formatted engagement string
    
    Examples:
        >>> format_engagement_display(42, 15)
        '42 upvotes, 15 comments (57 total interactions)'
    """
    total = upvotes + comments
    return f"{upvotes} upvotes, {comments} comments ({total} total interactions)"


def format_date_display(date_string: str) -> str:
    """Format date string for readable display.
    
    Args:
        date_string: ISO format date string
    
    Returns:
        str: Human-readable date
    
    Examples:
        >>> format_date_display('2024-11-23T10:30:00')
        'November 23, 2024'
    """
    try:
        dt = datetime.fromisoformat(date_string)
        return dt.strftime('%B %d, %Y')
    except ValueError:
        return date_string


# =============================================================================
# Test Data Collections
# =============================================================================

def get_test_suite() -> Dict[str, List[Dict[str, Any]]]:
    """Get a complete test suite with various post types.
    
    Returns:
        Dict: Collection of test posts organized by type
    """
    return {
        "academic_posts": [create_academic_post() for _ in range(3)],
        "humor_posts": [create_humor_post() for _ in range(3)],
        "misinformation_posts": [create_misinformation_post() for _ in range(2)],
        "mixed_posts": create_sample_posts(10),
        "weekly_posts": create_weekly_sample_data(),
        "semester_posts": create_semester_sample_data()
    }


if __name__ == "__main__":
    # Test sample data generation
    print("Reddit Analysis Utils - Testing Sample Data")
    print("=" * 50)
    
    # Test single post creation
    post = create_sample_post()
    print(f"\n✓ Sample post created: {post['title']}")
    print(f"  Category: {post['category']}, Engagement: {post['upvotes']} upvotes")
    
    # Test bulk post creation
    posts = create_sample_posts(5)
    print(f"\n✓ Generated {len(posts)} sample posts")
    
    # Test specialized posts
    academic = create_academic_post()
    humor = create_humor_post()
    misinfo = create_misinformation_post()
    print(f"\n✓ Created specialized posts:")
    print(f"  Academic: {academic['title']}")
    print(f"  Humor: {humor['title']}")
    print(f"  Misinformation: {misinfo['is_disinformation']}")
    
    # Test weekly data
    weekly = create_weekly_sample_data()
    print(f"\n✓ Generated weekly data: {len(weekly)} posts")
    
    print("\nUtils module loaded successfully!")

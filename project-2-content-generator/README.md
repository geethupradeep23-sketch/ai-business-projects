# Project 2: Content Generator 📝

## What it does
Generates multiple variations of content (social media posts, emails, blog ideas) based on a topic. Perfect for content creators and marketers.

## Use Cases
- **Social Media Manager:** Generate Instagram, Twitter, LinkedIn posts
- **Email Marketing:** Create subject lines and email body copies
- **Blogger:** Generate blog post ideas and outlines
- **Copywriter:** Create product descriptions and sales copy

## How to Run

```bash
cd project-2-content-generator
pip install -r requirements.txt
python app.py
```

Then open your browser to `http://localhost:5001`

## Code Explanation

1. **Multiple Content Types:** Generates different formats (posts, emails, etc.)
2. **Bulk Generation:** Creates multiple variations in one request
3. **Customizable Tone:** Can change writing style (professional, casual, humorous)
4. **Copy to Clipboard:** Easy one-click copying

## How to Customize

Edit the prompts in `app.py` to generate different content types:

```python
PROMPTS = {
    'instagram': 'Generate 3 Instagram captions about {topic}...',
    'email': 'Generate 3 email subject lines about {topic}...'
}
```

## Monetization Ideas

- **Free tier:** Generate 3 variations/day
- **Premium tier:** Unlimited generations, priority features
- **API access:** Let agencies integrate it
- **White-label:** Sell to social media agencies

## Next Steps

1. Try generating content for different topics
2. Add more content types (ad copy, product descriptions)
3. Add user authentication
4. Deploy on Render
5. Start selling API access

## Advanced Features to Add

- [ ] Save favorite generations
- [ ] A/B test generated content
- [ ] User accounts with saved history
- [ ] Integration with social media scheduling tools
- [ ] Template library
- [ ] Analytics (which content performs best)

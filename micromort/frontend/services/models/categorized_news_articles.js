const mongoose = require('mongoose');

const CategorizedNewsArticlesSchema  = new mongoose.Schema(
  {
    sentiment_category: {
      type: Number
    },
    article_url: String,
    article_text: String,
    article_id: Number,
    risk_category: [String],
    article_headline: String,
    date: Date
  },
  {
    collection: 'risk_categorized_news'
  }
)


const CategorizedNewsArticlesModel = mongoose.model('CategorizedNewsArticles', CategorizedNewsArticlesSchema);
module.exports = CategorizedNewsArticlesModel;

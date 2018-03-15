const errors = require('restify-errors');
const CategorizedNewsArticlesModel = require('../models/categorized_news_articles');
const async = require('async');
const lodashmap = require('lodash/map');
const pick = require('lodash/pick');
const partialRight = require('lodash/partialRight');
const join = require('lodash/join');
const split = require('lodash/split');
const countBy = require('lodash/countBy');
const sortBy = require('lodash/sortBy');
const toPairs = require('lodash/toPairs');
const take = require('lodash/take');
const englishStopWords =require('stopwords').english
const filter = require('lodash/filter');
const includes = require('lodash/includes');

module.exports = function(server) {

  server.get('/cna_date/:from_date/:to_date',
  function(req, res, next){
    const from_date = req.params.from_date;
    const to_date = req.params.to_date;

    //check whether dates have been sent in the desired format
    regex = new RegExp(/\d{4}-\d{2}-\d{2}/)

    const is_from_date_proper = regex.test(from_date);
    const is_to_date_proper = regex.test(to_date);

    if (!is_from_date_proper) {
      console.error('from_date passed is ' + from_date + ". It should be yyyy-mm-dd")
      var error = new errors.InvalidArgumentError({
        statusCode: 409
      }, 'from_date passed is ' + from_date + '. It should be yyyy-mm-dd')
      res.send(error)
      next()


    } else if (!is_to_date_proper) {
      var error = new errors.InvalidArgumentError({
        statusCode: 409
      }, 'to_date passed is ' + to_date + ". It should be yyyy-mm-dd")
      res.send(error)
      next()
    }

    // Query the database for the appropriate documents
    from_date_object = new Date(from_date);
    to_date_object = new Date(to_date)

    CategorizedNewsArticlesModel.find({
      'date': {
          '$gte': from_date_object,
          '$lt': to_date_object
       }
    }, function(error, docs){
      res.send(docs)
    })
  }) // end of get method

  server.get('/cna_date/:from_date/:to_date/:category',
  function(req, res, next){

    const from_date = req.params.from_date
    const to_date =  req.params.to_date
    const category = req.params.category
    //check whether dates have been sent in the desired format
    regex = new RegExp(/\d{4}-\d{2}-\d{2}/)

    const is_from_date_proper = regex.test(from_date);
    const is_to_date_proper = regex.test(to_date);

    if (!is_from_date_proper) {
      console.error('from_date passed is ' + from_date + ". It should be yyyy-mm-dd")
      var error = new errors.InvalidArgumentError({
        statusCode: 409
      }, 'from_date passed is ' + from_date + '. It should be yyyy-mm-dd')
      res.send(error)
      next()


    } else if (!is_to_date_proper) {
      var error = new errors.InvalidArgumentError({
        statusCode: 409
      }, 'to_date passed is ' + to_date + ". It should be yyyy-mm-dd")
      res.send(error)
      next()
    }

    // Query the database for the appropriate documents

    from_date_object = new Date(from_date)
    to_date_object = new Date(to_date)

    CategorizedNewsArticlesModel.find({
      'date': {
          '$gte': from_date_object,
          '$lt': to_date_object
       },
       'risk_category': {
         '$in': [category]
       }
    }, function(error, docs){
      res.send({
        'docs': docs
      })
    })

  })

  server.get('cna_date_hist/:from_date/:to_date',
  function(req, res, next) {
      const from_date = req.params.from_date
      const to_date =  req.params.to_date
      const category = req.params.category
      //check whether dates have been sent in the desired format
      regex = new RegExp(/\d{4}-\d{2}-\d{2}/)

      const is_from_date_proper = regex.test(from_date);
      const is_to_date_proper = regex.test(to_date);

      if (!is_from_date_proper) {date_view
        console.error('from_date passed is ' + from_date + ". It should be yyyy-mm-dd")
        var error = new errors.InvalidArgumentError({
          statusCode: 409
        }, 'from_date passed is ' + from_date + '. It should be yyyy-mm-dd')
        res.send(error)
        next()


      } else if (!is_to_date_proper) {
        var error = new errors.InvalidArgumentError({
          statusCode: 409
        }, 'to_date passed is ' + to_date + ". It should be yyyy-mm-dd")
        res.send(error)
        next()
      }

      var from_date_object = new Date(from_date);
      var to_date_object = new Date(to_date);
      var current_date = new Date(from_date);

      len_docs = []


      async.whilst(
        function() {return current_date.getTime() <= to_date_object.getTime()},
        function(cb) {
          var next_date = new Date(current_date)
          next_date.setDate(current_date.getDate() + 1 )

          CategorizedNewsArticlesModel.find({
            'date': {
                '$gte': current_date,
                '$lt': next_date
             }
          }, function(error, docs){
            len_docs.push(docs.length)
            current_date.setDate(current_date.getDate() + 1)
            cb(null)
          })
        }, function(){
          res.send({
            'len_docs': len_docs
          })
        }
      )


  })



  server.get('cna_date_wordcloud/:from_date/:to_date/:category',
  function(req, res, next){
    const from_date = req.params.from_date;
    const to_date = req.params.to_date;
    const category = split(req.params.category, ',');
    console.log(category)

    //check whether dates have been sent in the desired format
    regex = new RegExp(/\d{4}-\d{2}-\d{2}/)

    const is_from_date_proper = regex.test(from_date);
    const is_to_date_proper = regex.test(to_date);

    if (!is_from_date_proper) {
      console.error('from_date passed is ' + from_date + ". It should be yyyy-mm-dd")
      var error = new errors.InvalidArgumentError({
        statusCode: 409
      }, 'from_date passed is ' + from_date + '. It should be yyyy-mm-dd')
      res.send(error)
      next()


    } else if (!is_to_date_proper) {
      var error = new errors.InvalidArgumentError({
        statusCode: 409
      }, 'to_date passed is ' + to_date + ". It should be yyyy-mm-dd")
      res.send(error)
      next()
    }

    // Query the database for the appropriate documents
    from_date_object = new Date(from_date);
    to_date_object = new Date(to_date)

    CategorizedNewsArticlesModel.find({
      'date': {
          '$gte': from_date_object,
          '$lt': to_date_object
       },
       'risk_category': {
         '$in': category
       }
    }, function(error, docs){
        console.log('number of documents retrieved', docs.length)
        var article_texts = lodashmap(docs, partialRight(pick, 'article_text'));
        article_texts = lodashmap(article_texts, function(article_text){
          return article_text['article_text']
        })
        article_texts = join(article_texts, '');
        words =  split(article_texts, ' ')


        // remove the stopwords
        // it it taking a longgggggg time
        // words = filter(words, function(word){ return includes(stopwords, word)})

        counts = countBy(words)
        counts = sortBy(toPairs(counts), function(tuple){return tuple[1]}).reverse();
        counts = take(counts, 100)

        counts = counts.map(function(word_count_tuple){
          return {'text': word_count_tuple[0], 'value': word_count_tuple[1]}
        })

        // sort by the count and return the top n counts

        res.send({
          'counts': counts
        })


    })

  })
};

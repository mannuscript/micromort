const config = require('./config');
const restify = require('restify');
const mongoose = require('mongoose');
const restifyPlugins = require('restify').plugins;
const routes = require('./routes/index')

const server = restify.createServer({
  name: config.name,
  version: config.version,
});

server.use(restifyPlugins.jsonBodyParser({ mapParams: true }));
server.use(restifyPlugins.acceptParser(server.acceptable));
server.use(restifyPlugins.queryParser({ mapParams: true }));
server.use(restifyPlugins.fullResponse());
server.use(
  function crossOrigin(req,res,next){
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "X-Requested-With");
    return next();
  }
);


server.listen(config.port, function() {

  mongoose.Promise = global.Promise;
  mongoose.connect(config.db.uri);

  const db = mongoose.connection;

  db.on('error', function(err) {
    console.error(err);
    process.exit(1);
  })

  db.on('open', function() {
      routes(server)
      console.log("Connected to the database server at %s", config.db.uri)
  })
  console.log('%s listening at %s', server.name, server.url);
})

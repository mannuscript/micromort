module.exports = {
	name: 'API',
	env: process.env.NODE_ENV || 'development',
	port: process.env.PORT || 1234,
	base_url: process.env.BASE_URL || 'http://localhost:1234',
	db: {
		uri: process.env.MONGODB_URI || 'mongodb://172.29.33.45:27017/micromort',
	},
};

import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import Grid from 'material-ui/Grid';
import { Doughnut, Bar } from 'react-chartjs-2';
import  ChartCard  from '../cards/chart_card';
import data from '../../configs/data';


const dougnutData = data.doughnutData;

const landingComponentStyles = {
  container: {
    'marginTop': '25px'
  }
}
class LandingComponent extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      'doughnutData': {
        labels: [
          'Social Media',
          'Traditional Media',
        ],
        datasets: [{
      		data: [],
      		backgroundColor: [
      		'#FF6384',
      		'#36A2EB',
      		],
      		hoverBackgroundColor: [
      		'#FF6384',
      		'#36A2EB',
      		]
        }]
      },
      'barChartData':{
        labels: ['Health', 'Safety', 'Environment', 'Social Relations', 'Meaning in Life', 'Achievement', 'Economics', 'Politics'],
        datasets: [
          {
            label: '#Articles for different risk categories',
            backgroundColor: ['#F44336','#E91E63', '#9C27B0', '#3F51B5', '#009688',
          '#CDDC39', '#FF5722', 'blue'],
            borderColor: ['#F44336','#E91E63', '#9C27B0', '#3F51B5', '#009688',
          '#CDDC39', '#FF5722', 'blue'],
            borderWidth: 1,
            data: []
          }
        ]
      }
    }

    this.count_news_api_url = 'http://localhost:1234/num_cna';
    this.count_categories_api_url = 'http://localhost:1234/num_cna/';
    this.categories = ['health', 'safety_security', 'environment',
                  'social_relations', 'meaning_in_life', 'achievement',
                  'economics', 'politics'];
  }


  render() {
    const { classes } = this.props;
    return (
      <div className={classes.container}>
          <Grid container>

            <Grid item xs={12} sm={12} md={12}>
              <ChartCard
                chart={<Doughnut data={this.state.doughnutData}></Doughnut>}
                chartContentHeader={"Proportion of Social Media and Traditional Media News"}
                >
              </ChartCard>
            </Grid>

          </Grid>

          <Grid container>

            <Grid item xs={12} sm={12} md={6}>
              <ChartCard
                chart={<Bar data={data.chartjsBarChartData}></Bar>}
                chartContentHeader={"Volume of different risk categories in social media"}
                >
              </ChartCard>
            </Grid>

            <Grid item xs={12} sm={12} md={6}>
              <ChartCard
                chart={<Bar data={this.state.barChartData}></Bar>}
                chartContentHeader={"Volume of different risk categories in Traditional media"}
                >
              </ChartCard>
            </Grid>

          </Grid>
      </div>
    )
  }


  componentDidMount(){
    this.fetchData()
  }


  fetchData(){
    const that = this;
    fetch(this.count_news_api_url)
    .then(response => response.json())
    .then(function(count){
      var doughnutData = {...that.state.doughnutData}
      doughnutData.datasets[0]['data'] = [100, count['count']]
      that.setState({
        'doughnutData': doughnutData
      })
    })

    var categoryApiUrls = []
    this.categories.forEach(function(category) {
        categoryApiUrls.push(fetch(that.count_categories_api_url + '/' + category)
        .then(response => response.json()))
    })

    var num_articles_category = []
    Promise
    .all(categoryApiUrls)
    .then(all_data => {
      all_data.forEach(function(data) {
        num_articles_category.push(data['count'])
      })

      var barChartData = {...that.state.barChartData}
      barChartData.datasets[0]['data'] = num_articles_category;
      this.setState({
        'barChartData': barChartData
      })
    })


  }
}

export default withStyles(landingComponentStyles)(LandingComponent);

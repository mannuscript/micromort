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
      }
    }

    this.count_news_api_url = 'http://localhost:1234/num_cna'
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
                chart={<Bar data={data.chartjsBarChartData}></Bar>}
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
  }
}

export default withStyles(landingComponentStyles)(LandingComponent);

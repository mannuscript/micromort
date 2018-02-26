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
  render() {
    const { classes } = this.props;
    return (
      <div className={classes.container}>
          <Grid container>

            <Grid item xs={12} sm={12} md={12}>
              <ChartCard
                chart={<Doughnut data={dougnutData}></Doughnut>}
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
}

export default withStyles(landingComponentStyles)(LandingComponent);

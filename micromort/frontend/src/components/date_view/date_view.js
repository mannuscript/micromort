// This is the overarching component for the date view

import React from 'react';
import { Grid } from 'material-ui';
import { withStyles } from 'material-ui/styles';
import PropTypes from 'prop-types';
import DatePickers  from './date_picker';
import { dateViewStyles } from '../../configs/styles';
import ChartCard from '../cards/chart_card';
import SocialMediaSection from '../cards/social_media_section';
import ChartistGraph from 'react-chartist';
import  data  from '../../configs/data';
import  TagCloudCard from '../cards/word_cloud_card';


const barChartData = data.barChartData;
const lineChartData = data.lineChartData;
const lineChartOptions = data.lineChartOptions;


class DateView extends React.Component {
  render(){
    const { classes } = this.props
    return (
      <div className={classes.root}>
        <Grid container>
          <Grid item xs={12} sm={6} md={6}>
            <DatePickers label={"From"}></DatePickers>
          </Grid>
          <Grid item item xs={12} sm={6} md={6}>
            <DatePickers label={"To"}></DatePickers>
          </Grid>
        </Grid>

        <Grid container justify="center">
          <Grid item xs={12} sm={12} md={6}>
            <ChartCard
              chart={<ChartistGraph data={barChartData} type={'Bar'} />}
              chartContentHeader={"Traditional Media vs Social Media"}
              chartParagraphs={['Health has the highest News mentions',
            'Achievement has the highest Social Media Mentions']}
              >
              </ChartCard>
          </Grid>
          <Grid item xs={12} sm={12} md={6}>
            <ChartCard
              chart={<ChartistGraph data={lineChartData} type={'Line'}
              options={lineChartOptions}/>}
              chartContentHeader={"Total Number of News Mentions over time"}
              >
              </ChartCard>
          </Grid>

        </Grid>

        <Grid container justify="space-around">
          <Grid item xs={12} sm={12} md={6}>
            <SocialMediaSection></SocialMediaSection>
          </Grid>
          <Grid item xs={12} sm={12} md={6}>
            <TagCloudCard></TagCloudCard>
          </Grid>
        </Grid>

      </div>
    )
  }
}

DateView.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(dateViewStyles)(DateView)

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
import Button from 'material-ui/Button';


const barChartData = data.barChartData;
const lineChartData = data.lineChartData;
const lineChartOptions = data.lineChartOptions;


class DateView extends React.Component {

  constructor(props){
    console.log('inside the constructor')
      super(props);
      // Get the current date and pass it to the datepicker
      var today = new Date();
      var dd = today.getDate();
      var mm = today.getMonth() + 1;
      var yyyy = today.getFullYear();
      if(dd<10) {
        dd = '0'+dd
      }

      if(mm<10) {
          mm = '0'+mm
      }

      today = yyyy + '-' + mm + '-' + dd;

      var one_month_behind = new Date(today)
      one_month_behind.setMonth(one_month_behind.getMonth() - 1)
      var dd = one_month_behind.getDate()
      var mm = one_month_behind.getMonth() + 1
      var yyyy = one_month_behind.getFullYear()

      if(dd<10) {
        dd = '0'+dd
      }

      if(mm<10) {
          mm = '0'+mm
      }

      one_month_behind = yyyy + '-' + mm + '-' + dd;

      this.state = {
        'from_date': one_month_behind,
        'to_date': today,
        'news_all_line_chart_data': []
      }

      this.histApiUrl = 'http://localhost:1234/cna_date_hist/';
      this.setFromDate = this.setFromDate.bind(this);
      this.setToDate = this.setToDate.bind(this);
      this.fetchData = this.fetchData.bind(this);
  }

  componentDidMount() {
    const histApiUrl = this.histApiUrl + this.state.from_date + '/' + this.state.to_date
    fetch(histApiUrl)
    .then(response => response.json())
    .then((data) => {
      this.setState({
        'news_all_line_chart_data': {
          series: [data['len_docs']],
          labels: Array.from({length: data['len_docs'].length}, (x,i) => i)
        }
      })
    })
  }


  render(){
    const { classes } = this.props

    return (
      <div className={classes.root}>
        <Grid container>
          <Grid item xs={12} sm={5} md={5}>
            <DatePickers label={"From"}
            defaultValue={this.state.from_date}
            onChange={this.setFromDate}></DatePickers>
          </Grid>
          <Grid item item xs={12} sm={5} md={5}>
            <DatePickers label={"To"}
            defaultValue={this.state.to_date}
            onChange={this.setToDate}></DatePickers>
          </Grid>
          <Grid item xs={12} sm={2} md={2}>
          <Button variant="raised" color="primary" size="large"
          className={classes.button} onClick={this.fetchData}>
            Primary
          </Button>
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
              chart={<ChartistGraph data={this.state.news_all_line_chart_data} type={'Line'}
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


  setFromDate(date) {
    console.log('setting from date to ', date)
    this.setState({
      'from_date': date
    })
  }


  setToDate(date) {
    console.log('setting to date to', date);
    this.setState({
      'to_date': date
    })
  }


  fetchData(){
    const histApiUrl = this.histApiUrl + this.state.from_date + '/' + this.state.to_date
    fetch(histApiUrl)
    .then(response => response.json())
    .then((data) => {
      this.setState({
        'news_all_line_chart_data': {
          series: [data['len_docs']],
          labels: Array.from({length: data['len_docs'].length}, (x,i) => i)
        }
      })
    })
  }
}

DateView.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(dateViewStyles)(DateView)

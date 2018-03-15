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
import random from 'lodash/random';
import pullAt from 'lodash/pullAt';
import filter from 'lodash/filter';
import lodashmap from 'lodash/map';


const barChartData = data.barChartData;
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
        'news_all_line_chart_data': [],
        'news_category_bar_chart_data': [],
        chipData: [
          { key: 0, label: 'Health', selected: true },
          { key: 1, label: 'Safety', selected: false },
          { key: 2, label: 'Environment', selected: false },
          { key: 3, label: 'Social Relations', selected: false },
          { key: 4, label: 'Meaning in Life', selected: false },
          { key: 5, label: 'Achievements', selected: false },
          { key: 6, label: 'Economics', selected: false },
          { key: 7, label: 'Politics', selected: false },

        ],
        'wordCloudData': []
      }

      this.histApiUrl = 'http://localhost:1234/cna_date_hist/';
      this.cnaCategoryApiUrl = 'http://localhost:1234/cna_date/';
      this.wordCloudApiUrl = 'http://localhost:1234/cna_date_wordcloud/';
      this.categories = ['health', 'safety_security', 'environment',
                    'social_relations', 'meaning_in_life', 'achievement',
                    'economics', 'politics']
      this.setFromDate = this.setFromDate.bind(this);
      this.setToDate = this.setToDate.bind(this);
      this.fetchData = this.fetchData.bind(this);
      this.onChipClick = this.onChipClick.bind(this);
  }

  componentDidMount() {
    this.fetchData();
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
            Go
          </Button>
          </Grid>
        </Grid>

        <Grid container justify="center">
          <Grid item xs={12} sm={12} md={6}>
            <ChartCard
              chart={<ChartistGraph data={this.state.news_category_bar_chart_data}
              type={'Bar'} />}
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
            <TagCloudCard
              chipData={this.state.chipData}
              wordCloudData={this.state.wordCloudData}
              onChipClick={this.onChipClick}
            >
            </TagCloudCard>
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

    // query the line graph
    const histApiUrl = this.histApiUrl + this.state.from_date + '/' + this.state.to_date
    fetch(histApiUrl)
    .then(response => response.json())
    .then((data) => {
      this.setState({
        'news_all_line_chart_data': {
          series: [data['len_docs']],
          labels: []
        }
      })
    })

    // query the bar chart data for the bar graph
    var that = this;
    var categoryApiUrls = []
    this.categories.forEach(function(category) {
        categoryApiUrls.push(fetch(that.cnaCategoryApiUrl + that.state.from_date +
          '/' + that.state.to_date + '/' + category).then(response => response.json()))
    })
    var num_articles_category = []
    var num_social_media_category = []

    Promise
    .all(categoryApiUrls)
    .then(all_data => {
      all_data.forEach(function(data) {
        num_articles_category.push(data['docs'].length)
      })
      num_articles_category.forEach(function(num) {
        num_social_media_category.push(random(0, 100))
      })
      this.setState({
        'news_category_bar_chart_data': {
          'labels': ['Health', 'Safety/Security', 'Environment',
                        'Social Relations', 'Life Meaning', 'Achievement',
                        'Economics', 'Politics'],
          'series': [num_articles_category, num_social_media_category]
        }
      })
    })


    // query the word cloud graph
    var selected_chips = filter(this.state.chipData, {'selected': true});
    var selected_indices = lodashmap(selected_chips, function(selected_chip){
      return selected_chip['key']
    })
    var selected_classes = []
    selected_indices.forEach(function(index){
      selected_classes.push(that.categories[index])
    })
    const wordCloudApi = this.wordCloudApiUrl + this.state.from_date + '/' +
    this.state.to_date + '/' + selected_classes;

    fetch(wordCloudApi)
    .then(response => response.json())
    .then(function(wordCloudData){
      that.setState({
        'wordCloudData': wordCloudData['counts']
      })
    })

  }


  onChipClick(chipData){
    const that = this;
    var selected_chips = filter(this.state.chipData, {'selected': true});
    var selected_indices = lodashmap(selected_chips, function(selected_chip){
      return selected_chip['key']
    })

    var selected_classes = []
    selected_indices.forEach(function(index){
      selected_classes.push(that.categories[index])
    })

    const wordCloudApi = this.wordCloudApiUrl + this.state.from_date + '/' +
    this.state.to_date + '/' + selected_classes;

    fetch(wordCloudApi)
    .then(response => response.json())
    .then(function(wordCloudData){
      that.setState({
        'wordCloudData': wordCloudData['counts'],
        'chipData': chipData
      })
    })

  }

}

DateView.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(dateViewStyles)(DateView)

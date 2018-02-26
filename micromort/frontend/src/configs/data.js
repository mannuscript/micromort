// This is for configuring some of the static data that is required
// for the mockups and for some of the components like the sidedrawer
import React from 'react';
import { DateRange, List } from 'material-ui-icons'

const navigationDrawerMenuItems = [{
  'index': 0,
  'text': 'Date',
  'icon_class': <DateRange></DateRange>,
  'isSelected': false,
  'path': 'date_view'
}, {
  'index': 1,
  'text': 'Category',
  'icon_class': <List></List>,
  'isSelected': false,
  'path': 'category_view'
}]


const barChartData = {
  labels: ['Security', 'Health', 'Environment', 'Achievement', 'Economics'],
  series: [
    [100, 200, 150, 175, 120],
    [50, 100, 100, 125, 75],
  ]
}

const lineChartData = {
  labels: [1, 2, 3, 4, 5, 6, 7, 8],
  series: [
    [5, 9, 7, 8, 5, 3, 5, 4]
  ]
}


const lineChartOptions = {
  low: 0,
  showArea: true
}

var doughnutData = {
  labels: [
    'Social Media',
    'Traditional Media',
  ],
  datasets: [{
		data: [10000, 20000],
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

const chartjsBarChartData = {
  labels: ['Health', 'Safety', 'Environment', 'Social Relations', 'Meaning in Life', 'Achievement', 'Economics'],
  datasets: [
    {
      label: '#Articles for different risk categories',
      backgroundColor: ['#F44336','#E91E63', '#9C27B0', '#3F51B5', '#009688',
    '#CDDC39', '#FF5722'],
      borderColor: ['#F44336','#E91E63', '#9C27B0', '#3F51B5', '#009688',
    '#CDDC39', '#FF5722'],
      borderWidth: 1,
      data: [65, 59, 80, 81, 56, 55, 100]
    }
  ]
};


const data = {
  barChartData,
  chartjsBarChartData,
  doughnutData,
  lineChartData,
  lineChartOptions,
  navigationDrawerMenuItems,
}

export default data;

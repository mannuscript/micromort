//  This creates the chart card
import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import Card, { CardHeader, CardContent, CardActions  } from 'material-ui/Card';
import Typography from 'material-ui/Typography';


const chartCardStyles = {
  chartInformationHeading: {
    'font-family': "Roboto, Helvetica, Arial, sans-serif",
    'font-weight': 300,
    'font-size': '1.2em',
    "line-height": '1.5em',
    "color": 'rgba(251,140,0, 0.85)',
    'border-bottom': '1px dotted rgb(0,0,0,0.87)'
  },
  chartInformationParagraph: {
    'font-family': "Roboto, Helvetica, Arial, sans-serif",
    'font-weight': 300,
    'font-size': '0.85em',
    "line-height": '0.85em',
    "color": 'rgba(0, 0, 0, 0.85)',
  }
}


class ChartCard extends React.Component {
  render() {
    const { classes, chart, chartContentHeader, chartParagraphs,
    chartContentHeaderColor } = this.props;
    const chartHeader = chartContentHeader? chartContentHeader: null;
    const chartText = chartParagraphs? chartParagraphs: null
    return (
      <Card>
        <CardHeader
        subheader={chart}
        />

        {
          chartHeader?
          <CardContent>
              {chartHeader? (
                <p className={classes.chartInformationHeading}>{chartContentHeader}</p>
              ): ''}

              {chartText? chartText.map(text => {
                return <p className={classes.chartInformationParagraph}>{text}</p>
              }): ''}
          </CardContent>: ''

        }
      </Card>
    );
  }
}

ChartCard.propTypes = {
  classes: PropTypes.object.isRequired,
  chartContentHeaderColor: PropTypes.oneOf(['orange', 'red'])
}

export default withStyles(chartCardStyles)(ChartCard)

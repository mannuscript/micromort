// This craetes the card for social media
import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import { Grid, Paper, Typography } from 'material-ui';
import SocialMediaCard from './social_media_card';
import Share from 'material-ui-icons/Share';
import Card, { CardHeader, CardContent, CardActions } from 'material-ui/Card';
import Avatar from 'material-ui/Avatar';
import ReactPaginate from 'react-paginate';




const styles = {
  container: {
    display: 'flex',
    'flex-direction': 'column',
    'flex-wrap': 'wrap',
    'margin-top': '20px'
  },
  paper: {
    display: 'flex',
    'margin': '10px'
  },
  shareIcon: {
    'background-color': '#0084b4'
  },
  paginationWrapper: {
    'display': 'table-cell',
    'margin': '0 auto'
  },
  cardHeaderTitle: {
    'font-family': "Roboto, Helvetica, Arial, sans-serif",
    'font-weight': 550,
    'font-size': '1.2em',
    "line-height": '0.85em',
    "color": 'rgba(0, 0, 0, 0.85)',
    'font-variant': 'small-caps'
  }
}

class SocialMediaSection extends React.Component {
  constructor(props){
    super(props);
    this.state = {
      social_media_content: [],
      pageCount: 10,

    }
  }

  render() {
    const { classes } = this.props;

    return (
        <Card className={classes.container}>
          <CardHeader
            avatar={
              <Avatar className={classes.shareIcon}>
                <Share></Share>
              </Avatar>
            }
            title="Tweets"
            classes={{
              title: classes.cardHeaderTitle
            }}
          />
          <CardContent>
            <SocialMediaCard></SocialMediaCard>
            <SocialMediaCard></SocialMediaCard>
            <SocialMediaCard></SocialMediaCard>
          </CardContent>

          <div className={classes.paginationWrapper}>
            <ReactPaginate previousLabel={"<"}
                    nextLabel={">"}
                    breakLabel={<a>...</a>}
                    breakClassName={"break"}
                    pageCount={this.state.pageCount}
                    marginPagesDisplayed={2}
                    pageRangeDisplayed={2}
                    onPageChange={this.handlePageClick}
                    containerClassName={"pagination"}
                    subContainerClassName={"pages_pagination"}
                    activeClassName={"active"}
                    previousClassName={"previous"}/>
            </div>

        </Card>

    );
  }
}

SocialMediaSection.propTypes = {
  classes: PropTypes.object.isRequired
}


export default withStyles(styles)(SocialMediaSection);

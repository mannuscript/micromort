import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import Card, { CardHeader, CardContent } from 'material-ui/Card';
import Avatar from 'material-ui/Avatar';



const styles = {
  card: {    
    'margin-top': '2px',
  },
  avatar: {
    'background-color': 'red'
  }
}

class SocialMediaCard extends React.Component {
  render() {
    const { classes } = this.props;
    return (
      <div className={classes.card}>
        <Card>
          <CardHeader
            avatar={
              <Avatar className={classes.avatar}>
                R
              </Avatar>
            }
            title="This is a really really really really long long long tweet
            long long long long long long"
            subheader="September 14, 2016"
          />
        </Card>
      </div>
    );
  }
}

SocialMediaCard.propTypes = {
  classes: PropTypes.object.isRequired
}

export default withStyles(styles)(SocialMediaCard);

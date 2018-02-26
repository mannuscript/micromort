import React from 'react';
// import PropTypes from 'prop-types';
import { AppBar, Toolbar, IconButton, Typography, withStyles } from 'material-ui';
import  MenuIcon  from 'material-ui-icons/Menu';
import { appBarStyles } from '../configs/styles';


class ApplicationBar extends React.Component {
  render(){
    const { classes, onDrawerToggle } = this.props;
    return (
      <AppBar className={classes.root}>
        <Toolbar>
          <IconButton
            color="inherit"
            arial-label="Menu"
            onClick={() => {onDrawerToggle()}}>
            <MenuIcon/>
          </IconButton>
          <Typography variant="title" color="inherit">
            Risk Pulse Dashboard
          </Typography>
        </Toolbar>
      </AppBar>
  )
  }
}

export default withStyles(appBarStyles)(ApplicationBar)

import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import Grid from 'material-ui/Grid';
import { Route, Switch } from 'react-router-dom';
import NavigationDrawer from './navigation_drawer/navigation_drawer';
import DateView from './date_view/date_view';
import CategoryView from './category_view/category_view';
import { appGridStyles } from '../configs/styles';
import ApplicationBar from './app_bar';
import LandingComponent from './landing/landing_view'




class AppGrid extends React.Component {

  constructor(props) {
    super(props);
    this.handleDrawerToggle = this.handleDrawerToggle.bind(this);
  }

  render() {
    const { classes } = this.props;
    return (
      <div>
        <Grid container>
            <Grid item md={2} >
              <NavigationDrawer>
              </NavigationDrawer>
            </Grid>
            <Grid item md={10}>
              <Switch>
                <Route exact path="/" component={LandingComponent}></Route>
                <Route exact path="/date_view" component={DateView}></Route>
                <Route exact path="/category_view" component={CategoryView}></Route>
              </Switch>
            </Grid>
        </Grid>
      </div>
    );
  }

  handleDrawerToggle() {
    console.log(this.navigationDrawerComponent)
  }
}

AppGrid.propTypes = {
  classes: PropTypes.object.isRequired,
}

export default withStyles(appGridStyles)(AppGrid);

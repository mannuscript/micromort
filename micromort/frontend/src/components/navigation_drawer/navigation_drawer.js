import React from 'react';
import { PropTypes } from 'prop-types';
import { withStyles } from 'material-ui/styles';
import { Drawer, Divider, Hidden }
from 'material-ui';
import { Timeline } from 'material-ui-icons';
import NavigationDrawerItem from './navigation_drawer_item'
import { navigationDrawerStyles } from '../../configs/styles'
import  data  from '../../configs/data'




class  NavigationDrawer extends React.Component{

  constructor(props){
    super(props)
    this.classes = props.classes
    this.state = {
      menuItems: data.navigationDrawerMenuItems,
      mobileOpen: false
    }
  }


  renderMenuItem(i, text, iconclass, isSelected, path) {
      const that = this;
      return (
        <NavigationDrawerItem
          key={'menu-item-' + i}
          onClick={(i) => that.handleMenuItemClick(i)}
          iconclass={iconclass}
          text={text}
          selected={isSelected}
          menuItemIndex={i}
          path={path}
        />
      )
    }

  render() {
      const { classes } = this.props;
      const that = this;
      const menuItems = this.state.menuItems.map((menuItem, index) => {
        return (
          that.renderMenuItem(index, menuItem.text,
          menuItem.icon_class, menuItem.isSelected,
          menuItem.path)
        )
      })

      return (
        <div>
          <Hidden mdUp>
            <Drawer
              type="temporary"
              classes={{
                paper: classes.drawerPaper,
              }}
              open={this.state.mobileOpen}
              onClose={this.handleDrawerToggle}
              ModalProps={{
                keepMounted: true, // Better open performance on mobile.
              }}
              >

              <div className={classes.drawerHeader}>
                <span className={classes.projectLogo}>Risk <Timeline></Timeline></span>
              </div>
              <Divider />
              <div>
                {menuItems}
              </div>
            </Drawer>
          </Hidden>
          <Hidden smDown implementation="css">

            <Drawer
              type="permanent"
              open
              classes={{
                paper: classes.drawerPaper,
              }}
              >

              <div className={classes.drawerHeader}>
                <span className={classes.projectLogo}>Risk <Timeline></Timeline></span>
              </div>
              <Divider />
              <div>
                {menuItems}
              </div>
            </Drawer>
          </Hidden>
        </div>
      );
    }

    handleMenuItemClick(i) {
      // change the state of the menu item that is clicked
      const menuItems = this.state.menuItems.slice()
      for(let [index, value] of menuItems.entries()) {
        if(index === i) {
          value['isSelected'] = true
        } else {
          value['isSelected'] = false
        }
      }
      this.setState({
        menuItems: menuItems
      })
    }


    handleDrawerToggle() {
      this.setState({ mobileOpen: !this.state.mobileOpen })
    }

}

NavigationDrawer.propTypes = {
  classes: PropTypes.object.isRequired
}

export default withStyles(navigationDrawerStyles)(NavigationDrawer)

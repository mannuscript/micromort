import React from 'react'
import { ListItem, ListItemIcon, ListItemText } from 'material-ui/List';
import { PropTypes } from 'prop-types';
import { withStyles } from 'material-ui/styles';
import { Link } from 'react-router-dom';
import { navigationDrawerItemStyles } from '../../configs/styles.js';


class NavigationDrawerItem extends React.Component {

  render(){
    const iconclass = this.props.iconclass;
    const text = this.props.text;
    const classes = this.props.classes;
    const textStyle = this.props.selected? classes.selectedText:
    classes.unselectedText;
    const menuItemIndex = this.props.menuItemIndex;
    const onMenuItemClick = this.props.onClick;
    const path = this.props.path


    return (
      <Link to={path} className={classes.item}>
        <ListItem button
          onClick={() => onMenuItemClick(menuItemIndex)}
          className={textStyle}>
          <ListItemIcon>
            {iconclass}
          </ListItemIcon>
            <ListItemText primary={text} disableTypography
            />
        </ListItem>
      </Link>
    )
  }
}


NavigationDrawerItem.propTypes = {
  classes: PropTypes.object.isRequired,
  iconclass: PropTypes.node,
  text: PropTypes.string,
  selected: PropTypes.bool,
  menuItemIndex: PropTypes.number,
  onMenuItemClick: PropTypes.func,
  path: PropTypes.string
}

export default withStyles(navigationDrawerItemStyles)(NavigationDrawerItem)

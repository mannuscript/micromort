import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import TextField from 'material-ui/TextField';

const styles = theme => ({
  container: {
    display: 'flex',
    flexWrap: 'wrap',
  },
  textField: {
    marginLeft: theme.spacing.unit,
    marginRight: theme.spacing.unit,
    width: 200,
  },
});

class  DatePickers extends React.Component{
  constructor(props) {
    super(props);
    this.handleDate = this.handleDate.bind(this);
  }

  render(){
      const { classes, label, defaultValue } = this.props;

      return (
        <form className={classes.container} noValidate>
          <TextField
            label={label}
            type="date"
            defaultValue={defaultValue}
            className={classes.textField}
            InputLabelProps={{
              shrink: true,
            }}
            onChange={this.handleDate}
          />
        </form>
      );
  }

  handleDate(event, date) {
    this.props.onChange(event.target.value)
  }

}

DatePickers.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(DatePickers);

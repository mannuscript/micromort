import React from 'react';
import PropTypes from 'prop-types';

const divStyle = {
  'border': '1px solid #e0e0e0',
  'borderRadius': '16px',
  'padding': '5px 10px',
  'margin': '5px',
  'backgroundColor': '#e0e0e0',
   color: 'rgba(0, 0, 0, 0.75)',
   "fontFamily": "Roboto, Helvetica",
   "fontSize": "0.7rem",
   "lineHeight": "1.5em",
   'cursor': 'pointer'
}

const divStyleSelected = {
  'border': '1px solid #e0e0e0',
  'borderRadius': '16px',
  'padding': '5px 10px',
  'margin': '5px',
  'backgroundColor': '#388e3c',
   color: 'rgba(0, 0, 0, 0.75)',
   "fontFamily": "Roboto, Helvetica",
   "fontSize": "0.7rem",
   "lineHeight": "1.5em",
   'cursor': 'pointer'
}



class CustomChip extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const { text, isSelected, onClick, chipNumber } = this.props;
    return (
      <div style={isSelected? divStyleSelected: divStyle}
        onClick={() => onClick(chipNumber)}>
        <span>{text}</span>
      </div>
    )
  }
}

export default CustomChip;

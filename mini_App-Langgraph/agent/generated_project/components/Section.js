import React from 'react';

class Section extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className='section'>
        <header className='section-header'>
          {this.props.children}
        </header>
      </div>
    );
  }
}

export default Section;

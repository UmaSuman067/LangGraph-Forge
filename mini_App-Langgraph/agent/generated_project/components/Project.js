import React from 'react';

class Project extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div className="project">
        <h2>{this.props.title}</h2>
        <p>{this.props.description}</p>
        <img src={this.props.image} alt="Project Image"/>
      </div>
    );
  }
}

export default Project;

import React from 'react';
import Section from './Section';

class About extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <Section>
        <div className='about'>
          <h2>About Us</h2>
          <p>We are a team of dedicated professionals passionate about delivering high-quality solutions.</p>
          <p>For more information, please contact us at:</p>
          <ul>
            <li>Phone: 123-456-7890</li>
            <li>Email: <a href='mailto:info@example.com'>info@example.com</a></li>
          </ul>
        </div>
      </Section>
    );
  }
}

export default About;

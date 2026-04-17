import React from 'react';
import Section from './Section';

class Contact extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <Section>
        <div className="contact">
          <h2>Contact Us</h2>
          <form>
            <label>Name:</label>
            <input type="text" />
            <br />
            <label>Email:</label>
            <input type="email" />
            <br />
            <label>Message:</label>
            <textarea />
            <br />
            <button type="submit">Submit</button>
          </form>
        </div>
      </Section>
    );
  }
}

export default Contact;

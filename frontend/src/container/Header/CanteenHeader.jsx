import React from 'react';
import {images} from '../../constants'

import './CanteenHeader.css';
import { SubHeading } from '../../components';

const CanteenHeader = () => (
  <div className='app__header app__wrapper section__padding' id='home'>
    <div className="app__wrapper_info">
      <SubHeading title="Chase the new ordering experience"/>
      <h1 className="app__header-h1">The Key to Fine Dining</h1>
      <p className="p__opensans" style={{ margin: '2rem 0' }}>Seamless digital ordering for faster, smarter service.</p>
    </div>
    <div className="app__wrapper_img">
      <img src={images.welcome} alt="header img" />
    </div>
  </div>
);

export default CanteenHeader;

import React from 'react';
import { Outlet, useNavigate} from 'react-router-dom';
import { useEffect } from 'react';

const Classification = () => {

  const navigate = useNavigate();

  // useEffect hook to navigate to the 'file-download' page on component mount
  useEffect(() => {
    navigate('/app/classification/file-download');
  }, []); // Empty dependency array ensures this runs only once when the component mounts

  return (
    <div className="classification-page"> {/* Main container for the classification page */}
      <Outlet />
    </div>
  );
};

export default Classification
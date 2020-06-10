import React from "react";
import "./landing.css";
import developerWoman from  "../../assets/developer-woman.svg";
import Wireframe from "../../assets/Wireframe.png";
import "@fortawesome/fontawesome-free/css/all.css"; 

export default function Landing () {
    return (
        <>
        <section id="main_content" className="fore m-0">
            <div className="curved-div-1">
                <div className="container">
                    <div className="row justify-content-lg-center align-items-lg-center">
                        <div className="col-md-6 text-left" style={{"color": "white"}}>
                            <h2 className="display-4 mt-5 mb-3" style={{"font-size":"2.5em"}}>
                                <strong>Bridging the gender diversity gap in Tech</strong>
                            </h2>
                            
                            <p className="lead" style={{"color":"rgba(255, 255, 255, 0.5)"}}>
                                Get financing to pursue your career in Technology. 
                            </p>

                            <div className="pt-4">
                                <a href="#" className="btn btn-cta lift-sm rounded-pill">
                                    Get financing
                                    <i className="fas fa-arrow-right ml-1"></i> 
                                </a>
                                <a class="btn btn-link" href="#">Lend as an Investor ></a>
                            </div>
                        </div>

                        <div className="col-md-6 text-center pt-5" style={{"color": "white"}}>
                            <div>
                                <img class="imgdevWoman" src={developerWoman}  alt="" width="80%"/>
                            </div>
                        </div>
                    </div>
                </div>

                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320">
                    <path fill="#dfdfdf" fill-opacity="1" d="M0,288L48,282.7C96,277,192,267,288,245.3C384,224,480,192,576,170.7C672,149,768,139,864,138.7C960,139,1056,149,1152,138.7C1248,128,1344,96,1392,80L1440,64L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
                </svg>
            </div>
        </section>

        <section className="bg-light-grey m-0">
            <div className="curved-div-2">
                <div className="container">
                    <div className="row" align="center">
                        <div className="col-md-6">
                            <img className="img-section" src={Wireframe} alt="" />
                        </div>
                        <div className="col-md-6 dflex align-items-center justify-content-middle ">
                            <h2>diversity in Tech</h2>
                        </div>
                    </div>
                </div>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320">
                    <path fill="#fff" fill-opacity="1" d="M0,288L48,282.7C96,277,192,267,288,245.3C384,224,480,192,576,170.7C672,149,768,139,864,138.7C960,139,1056,149,1152,138.7C1248,128,1344,96,1392,80L1440,64L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
                </svg>
            </div>
        </section>

        <section className="bg-white py-3 d-flex align-items-center justify-content-center">
            <div className="container">
                <div className="row" align="center">
                    
                    <div className=" dflex align-items-center justify-content-middle col-md-6">
                        
                        <h2>diversity in Tech</h2>
                    </div>
                    <div className="col-md-6">
                        <img className="img-section" src={Wireframe} alt="" />
                    </div>
                </div>
            </div>
        </section>

        </>
    )
}


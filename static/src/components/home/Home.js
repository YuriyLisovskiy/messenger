import React, { Component } from 'react';
import '../../../css/index.css'
import '../../../css/bootstrap_social.css'

class Home extends Component {
	render() {
		return (
			<div className="content">
				<div className="left">
					<div className="site-description">
						<h3>Site Description</h3>
					</div>
				</div>
				<div className="right">
					<div className="contacts">
						<h3>Contacts</h3>
						<table>
							<tr>
								<th>Support:</th>
								<th>
									<a target="_blank" href="https://mail.google.com/mail/?view=cm&fs=1&to=mymessengerhelp@gmail.com">Messenger
									</a>
								</th>
							</tr>
							<tr>
								<th>Administrator:</th>
								<th>
									<a target="_blank" href="https://mail.google.com/mail/?view=cm&fs=1&to=yuralisovskiy98@gmail.com">
										Yuriy Lisovskiy
									</a>
								</th>
							</tr>
						</table>
						<h3>Share</h3>
						<div className="other-login-methods">
							<button id="google-login" title="Share on Google+" className="btn login-social btn-social-icon btn-google">
								<span className="fa fa-google-plus"></span>
							</button>
							<div title="Share on Facebook" data-href="http://127.0.0.1:8000/" data-layout="button_count" data-size="large" data-mobile-iframe="true">
								<a className="btn login-social btn-social-icon btn-facebook" target="_blank" href="https://www.facebook.com/sharer/sharer.php?u=http%3A%2F%2F127.0.0.1%3A8000%2F&amp;src=sdkpreparse">
									<span className="fa fa-facebook"></span>
								</a>
							</div>
							<button id="twitter-login" title="Share on Twitter" className="btn login-social btn-social-icon btn-twitter">
								<span className="fa fa-twitter"></span>
							</button>
						</div>
					</div>
				</div>
			</div>
		);
	}
}

export default Home;

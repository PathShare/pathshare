import { Component, OnInit} from '@angular/core';
import { NgForm } from '@angular/forms';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html',
  styleUrls: ['./signup.component.css']
})
export class SignupComponent implements OnInit {

  constructor(private authService: AuthService) { }

  ngOnInit() {
  }

  onSignup(form: NgForm) {
    const name = form.value.name;
    const major = form.value.major;
    const age = form.value.age;
    const username = form.value.username;
    const email = form.value.email;
    const password = form.value.password;

    this.authService.signupUser(name,major,age,username,email,password);
  }

}

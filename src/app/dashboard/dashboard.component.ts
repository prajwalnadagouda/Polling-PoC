import { Component, OnInit } from '@angular/core';
import { Course } from '../hero';
import { HeroService } from '../hero.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: [ './dashboard.component.css' ]
})
export class DashboardComponent implements OnInit {
  courses: Course[] = [];

  constructor(private heroService: HeroService) { }

  ngOnInit() {
    this.getHeroes();
  }

  getHeroes(): void {
    // this.heroService.testService();
    this.heroService.getHeroes()
      .subscribe(courses => this.courses = courses);
  }
}

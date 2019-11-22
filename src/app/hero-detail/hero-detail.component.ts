import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';

import { Course }         from '../hero';
import { HeroService }  from '../hero.service';

@Component({
  selector: 'app-hero-detail',
  templateUrl: './hero-detail.component.html',
  styleUrls: [ './hero-detail.component.css' ]
})
export class HeroDetailComponent implements OnInit {
  @Input() course: Course;
  constructor(
    private route: ActivatedRoute,
    private heroService: HeroService,
    private location: Location,
  ) {}
  // videos:["https://www.youtube.com/watch?v=6vE0oFFSE7c","https://www.youtube.com/watch?v=6vE0oFFSE7c"];
  ngOnInit(): void {
    this.getHero();
  }

  // openpdf(event){
  //   let filename = (event.target.innerHTML);
  //   // this.heroService.openPDF(filename).subscribe();
  //   this.heroService.openPDF(filename).subscribe(
  //       (res) => {
  //       var fileURL = URL.createObjectURL(res);
  //       window.open(fileURL);
  //       }
  //   );
  // }
  fileUpload(fileInput: any): void{
    const id = +this.route.snapshot.paramMap.get('id');
    if (fileInput.target.files && fileInput.target.files[0]){
      this.heroService.uploadDoc(id, fileInput.target.files[0]).subscribe();
    }
  }

  getHero(): void {
    const id = +this.route.snapshot.paramMap.get('id');
    this.heroService.getHero(id)
      .subscribe(course => {
        this.course = course;
        this.longPoll();
      });
    // this.heroService.testService();
  }

  longPoll(): void{
    const id = +this.route.snapshot.paramMap.get('id');
    this.heroService.longPoll(id)
      .subscribe(course => {
        this.course = course;
        this.longPoll();
      });
  }

  goBack(): void {
    this.location.back();
  }
}

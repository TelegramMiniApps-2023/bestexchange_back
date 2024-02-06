window.addEventListener('load', function () {
    let direction = document.getElementById('id_direction');
    let percent = document.getElementById('id_percent');
    let fix_amount = document.getElementById('id_fix_amount');
    let readonly = document.getElementsByClassName('readonly');
    // let final_amount = document.getElementById('id_final_amount');
    let course = readonly[0];
    let in_count = readonly[1];
    let out_count = readonly[2];

    get_valid_values();

    function get_valid_values() {
      let selectedDirection = direction.options[direction.selectedIndex].text;
      let course_value = 0;
      // console.log(selectedDirection);
      let direction_name = selectedDirection.split(' -> ');
      if (direction_name.length == 1) {
        course.textContent = String(course_value);
        // final_amount.value = Number(0);
        // final_value = 0;
        edit_in_out(course_value);
      } 
      else {
        let valute_from = direction_name[0];
        let valute_to = direction_name[1];
        // fetch(`http://localhost:8000/api/actual_course?valute_from=${valute_from}&valute_to=${valute_to}`)
        fetch(`https://wttonline.ru/api/actual_course?valute_from=${valute_from}&valute_to=${valute_to}`)
        .then(data => data.json())
        .then((text) => {
            console.log(text);
            course.textContent = String(text);
            // let course = text.data.amount;
            let percent_val = Number(percent.value);
            let fix_amount_val = Number(fix_amount.value);
            // console.log(course);
            // final_amount.value = Number(course);
            edit_in_out(text, percent_val, fix_amount_val);

            // edit_in_out(course, percent_val, fix_amount_val);
          })
      }
    }
    
    direction.addEventListener('change', (event) => {
      get_valid_values();
    })

    percent.addEventListener('input', (event) => {
      let course_val = Number(course.textContent);
      // let course = Number(final_amount.value);
      let percent_val = Number(percent.value);
      let fix_amount_val = Number(fix_amount.value);

      edit_in_out(course_val, percent_val, fix_amount_val);

      // edit_in_out(course, percent_val, fix_amount_val);
    })
    
    fix_amount.addEventListener('input', (event) => {
      let course_val = Number(course.textContent);
      // let course = Number(final_amount.value);
      let percent_val = Number(percent.value);
      let fix_amount_val = Number(fix_amount.value);
      edit_in_out(course_val, percent_val, fix_amount_val);

      // edit_in_out(course, percent_val, fix_amount_val);
  })

  function edit_in_out(course_val, percent_val = 0, fix_amount_val = 0) {
    if (course_val == 0) {
      in_count.textContent = String(0);
      out_count.textContent = String(0);
    } 
    else if (course_val < 1) {
      let k = 1 / course_val;
      let plus_percent = k * percent_val / 100;
      // let result = k + plus_percent + fix_amount_val;
      let result = k + plus_percent + fix_amount_val;

      in_count.textContent = String(result.toFixed(6));
      out_count.textContent = String(1);
    } 
    else {
      let plus_percent = Number(course.textContent) * percent_val / 100;
      let result = Number(course.textContent) - plus_percent - fix_amount_val;

      in_count.textContent = String(1);
      out_count.textContent = String(result);
    }
  }
})
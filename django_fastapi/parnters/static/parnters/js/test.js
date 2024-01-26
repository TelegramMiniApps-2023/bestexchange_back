window.addEventListener('load', function () {
    let direction = document.getElementById('id_direction');
    let percent = document.getElementById('id_percent');
    let fix_amount = document.getElementById('id_fix_amount');
    let course = document.getElementsByClassName('readonly')[0];
    course_value = Number(course.textContent);
    console.log(course_value);
    fix_amount.value = course_value + (course_value * percent.value / 100);
    
    direction.addEventListener('change', (event) => {
        let x = direction.options[direction.selectedIndex].text;
        console.log(x);
        fetch(`https://api.coinbase.com/v2/prices/rub-USDT/spot`)
        .then(data => data.json())
        .then((text) => {
            console.log(text);
            let ww = text.data.amount;
            console.log(ww);
            course.textContent = String(ww);
            fix_amount.value = ww + (ww * percent.value / 100);
        })
    })

    percent.addEventListener('input', (event) => {
        course_value = Number(course.textContent)
        fix_amount.value = course_value + (course_value * percent.value / 100);
    })
    
  })
console.log('22')

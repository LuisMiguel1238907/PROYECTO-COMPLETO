const handleSubmit = (e) => {
  e.preventDefault();

  const emailInput = e.currentTarget.querySelector('input[name="email"]');
  const email = emailInput?.value;

  if (email) {
    localStorage.setItem('userEmail', email);
    navigate('/dashboard');
  }
};

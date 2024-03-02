using Microsoft.EntityFrameworkCore;

public class PersonaContext : DbContext
{
    public PersonaContext(DbContextOptions<PersonaContext> options)
        : base(options)
    {
    }

    public DbSet<Persona> Personas { get; set; }
}

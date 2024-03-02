using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

[Route("api/[controller]")]
[ApiController]
public class PersonaController : ControllerBase
{
    private readonly PersonaContext _context;

    public PersonaController(PersonaContext context)
    {
        _context = context;
    }

    // GET: api/Persona
    [HttpGet]
    public async Task<ActionResult<IEnumerable<Persona>>> GetPersonas()
    {
        return await _context.Personas.ToListAsync();
    }

    // GET: api/Persona/5
    [HttpGet("{id}")]
    public async Task<ActionResult<Persona>> GetPersona(int id)
    {
        var persona = await _context.Personas.FindAsync(id);

        if (persona == null)
        {
            return NotFound();
        }

        return persona;
    }

    // POST: api/Persona
    [HttpPost]
    public async Task<ActionResult<Persona>> PostPersona(Persona persona)
    {
        _context.Personas.Add(persona);
        await _context.SaveChangesAsync();

        return CreatedAtAction(nameof(GetPersona), new { id = persona.Id }, persona);
    }

    // PUT: api/Persona/5
    [HttpPut("{id}")]
    public async Task<IActionResult> PutPersona(int id, Persona persona)
    {
        if (id != persona.Id)
        {
            return BadRequest();
        }

        _context.Entry(persona).State = EntityState.Modified;
        await _context.SaveChangesAsync();

        return NoContent();
    }

    // DELETE: api/Persona/5
    [HttpDelete("{id}")]
    public async Task<IActionResult> DeletePersona(int id)
    {
        var persona = await _context.Personas.FindAsync(id);

        if (persona == null)
        {
            return NotFound();
        }

        _context.Personas.Remove(persona);
        await _context.SaveChangesAsync();

        return NoContent();
    }
}

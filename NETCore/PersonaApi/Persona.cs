using System.ComponentModel.DataAnnotations;

public class Persona
{
    [Key]
    public int Id { get; set; }

    [Required]
    [StringLength(16)]
    public string? NumeroIdentificacion { get; set; }

    [Required]
    [StringLength(64)]
    public string? Nombre { get; set; }

    [Required]
    [StringLength(64)]
    [EmailAddress]
    public string? Email { get; set; }

    [Required]
    public bool Activo { get; set; }
}

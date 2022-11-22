package ec.xpd.apcisnomina.entidades;

import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.JoinColumn;
import javax.persistence.ManyToOne;
import javax.persistence.Table;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import javax.persistence.Column;
import java.util.Date;

@Entity
@Table(name="departments")
@JsonIgnoreProperties("hibernateLazyInitializer")
public class Department {
	@Id
	@GeneratedValue(strategy =  GenerationType.IDENTITY)
	@Column(name = "id")
	private Integer id;
	
	@Column(name = "created_by")
	private String createdBy;
	
	@Column(name = "created_date")
	private Date createdDate;
	
	@Column(name = "modified_by")
	private String modifiedBy;
	
	@Column(name = "modified_date")
	private Date modifiedDate;
	
	@Column(name = "status")
	private Boolean status;
	
	@Column(name = "description")
	private String description;
	
	@Column(name = "name")
	private String name;
	
	@Column(name = "phone")
	private String phone;

	@Column(name = "id_enterprise")
	private int idEnterprise;
	
	@ManyToOne( fetch = FetchType.LAZY )
	@JoinColumn( name="id_enterprise" , insertable=false, updatable=false)
	private Enterprise enterprise;

	public Integer getId() {
		return id;
	}

	public void setId(Integer id) {
		this.id = id;
	}

	public String getCreatedBy() {
		return createdBy;
	}

	public void setCreatedBy(String createdBy) {
		this.createdBy = createdBy;
	}

	public Date getCreatedDate() {
		return createdDate;
	}

	public void setCreatedDate(Date createdDate) {
		this.createdDate = createdDate;
	}

	public String getModifiedBy() {
		return modifiedBy;
	}

	public void setModifiedBy(String modifiedBy) {
		this.modifiedBy = modifiedBy;
	}

	public Date getModifiedDate() {
		return modifiedDate;
	}

	public void setModifiedDate(Date modifiedDate) {
		this.modifiedDate = modifiedDate;
	}

	public Boolean getStatus() {
		return status;
	}

	public void setStatus(Boolean status) {
		this.status = status;
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getPhone() {
		return phone;
	}

	public void setPhone(String phone) {
		this.phone = phone;
	}

	public Enterprise getEnterprise() {
		return enterprise;
	}

	public void setEnterprise(Enterprise enterprise) {
		this.enterprise = enterprise;
	}

	public int getIdEnterprise() {
		return idEnterprise;
	}

	public void setIdEnterprise(int idEnterprise) {
		this.idEnterprise = idEnterprise;
	}
	
}
